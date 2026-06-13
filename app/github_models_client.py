"""AI Models API client for LLM integration (OpenAI compatible)."""

import json
import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class GitHubModelsClient:
    """Client for GitHub Models API."""

    def __init__(self, token: str, base_url: str = "https://api.openai.com"):
        """Initialize GitHub Models client."""
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str | None:
        """Create chat completion using GitHub Models API."""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0,
                )
                response.raise_for_status()

                result = response.json()
                return result["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from GitHub Models API: {e}")
            return None
        except Exception as e:
            logger.error(f"Error calling GitHub Models API: {e}")
            return None

    async def improve_issue(self, title: str, repo_context: str | None = None) -> dict[str, Any] | None:
        """Improve issue title using GitHub Models."""
        prompt = self._build_improve_prompt(title, repo_context)

        messages = [
            {"role": "system", "content": "You are an expert GitHub issue improver. Always respond in JSON format."},
            {"role": "user", "content": prompt}
        ]

        response = await self.chat_completion(messages)
        if not response:
            return None

        try:
            # Try to extract JSON from response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end != -1:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                logger.error("No JSON found in response")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None

    def _build_improve_prompt(self, title: str, repo_context: str | None = None) -> str:
        """Build prompt for issue improvement."""
        base_prompt = f"""Given this GitHub issue title: "{title}"

Generate a comprehensive improvement in JSON format with:
- description: Detailed description of the issue
- reproduction_steps: Step-by-step how to reproduce
- expected_behavior: What should happen
- labels: Suggested labels (comma-separated, max 5)
- priority: low/medium/high
- assignee_suggestion: Suggested assignee if applicable

Example format:
{{
    "description": "Detailed explanation...",
    "reproduction_steps": "1. Step one\n2. Step two\n3. Step three",
    "expected_behavior": "Expected outcome...",
    "labels": "bug,ui,high-priority",
    "priority": "high",
    "assignee_suggestion": "username or null"
}}"""

        if repo_context:
            base_prompt += f"\n\nRepository context: {repo_context}"

        return base_prompt

    @staticmethod
    def from_env() -> "GitHubModelsClient":
        """Create GitHub Models client from environment variables."""
        token = os.getenv("GITHUB_MODELS_TOKEN")
        if not token:
            raise ValueError("GITHUB_MODELS_TOKEN environment variable is required")
        return GitHubModelsClient(token)
