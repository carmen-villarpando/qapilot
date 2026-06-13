#!/usr/bin/env python3
"""
QAPilot with Ollama - ZERO COST LLM-powered issue improvement
"""

import os
import json
import logging
from typing import Dict, Any

from github_client import GitHubClient
from ollama_client import OllamaClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QAPilotOllama:
    def __init__(self):
        self.github_client = GitHubClient()
        self.ollama_client = OllamaClient()
        
    def improve_issue_with_ollama(self, repo_name: str, issue_number: int) -> bool:
        """Improve GitHub issue using local Ollama model."""
        try:
            # Get issue data
            issue = self.github_client.get_issue(repo_name, issue_number)
            if not issue:
                logger.error(f"Could not retrieve issue #{issue_number}")
                return False
            
            # Detect issue type and generate prompt
            issue_type = self._detect_issue_type(issue.title, issue.body)
            prompt = self._generate_prompt(issue.title, issue.body, issue_type)
            
            # Generate improved content with Ollama
            improved_content = self.ollama_client.generate_response(prompt)
            
            if not improved_content:
                logger.error("Failed to generate improved content with Ollama")
                return False
            
            # Parse the improved content
            improvements = self._parse_ollama_response(improved_content, issue.title, issue_type)
            
            # Apply improvements
            success = self.github_client.update_issue(
                repo_name=repo_name,
                issue_number=issue_number,
                title=improvements.get("improved_title", issue.title),
                body=improvements.get("improved_body", issue.body),
                labels=improvements.get("labels", [])
            )
            
            if success:
                logger.info(f"Successfully improved issue #{issue_number}")
                return True
            else:
                logger.error(f"Failed to update issue #{issue_number}")
                return False
                
        except Exception as e:
            logger.error(f"Error improving issue: {e}")
            return False
    
    def _detect_issue_type(self, title: str, body: str) -> str:
        """Detect if issue is a bug or user story."""
        title_lower = title.lower()
        body_lower = body.lower()
        
        bug_keywords = ["bug", "error", "fix", "broken", "crash", "issue", "problem", "doesn't work"]
        story_keywords = ["feature", "add", "create", "implement", "user story", "enhancement"]
        
        for keyword in bug_keywords:
            if keyword in title_lower or keyword in body_lower:
                return "bug"
        
        for keyword in story_keywords:
            if keyword in title_lower or keyword in body_lower:
                return "story"
        
        return "auto"  # Default to auto-detection
    
    def _generate_prompt(self, title: str, body: str, issue_type: str) -> str:
        """Generate prompt for Ollama based on issue type."""
        
        if issue_type == "bug":
            prompt = f"""You are a Senior QA Lead. Improve this GitHub bug report to be professional and clear.

Original Title: {title}
Original Body: {body}

Please provide:
1. A corrected, professional title (fix any typos, use sentence case)
2. A comprehensive bug description with:
   - Clear problem description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Priority assessment

Format your response as JSON:
{{
  "improved_title": "corrected title here",
  "improved_body": "complete improved description here",
  "labels": ["bug", "needs-investigation"],
  "priority": "high|medium|low"
}}

Make it sound like a professional QA engineer wrote it. Be thorough but concise."""
        
        else:  # story or auto
            prompt = f"""You are a Product Owner/Project Manager. Improve this GitHub user story to be professional and clear.

Original Title: {title}
Original Body: {body}

Please provide:
1. A corrected, professional title (fix any typos, use sentence case)
2. A comprehensive user story with:
   - Clear user story format
   - Business context
   - Acceptance criteria
   - Dependencies and risks

Format your response as JSON:
{{
  "improved_title": "corrected title here",
  "improved_body": "complete improved user story here",
  "labels": ["feature", "story"],
  "priority": "high|medium|low"
}}

Make it sound like a professional product manager wrote it. Focus on user value and clear requirements."""
        
        return prompt
    
    def _parse_ollama_response(self, response: str, original_title: str, issue_type: str) -> Dict[str, Any]:
        """Parse Ollama response and extract improvements."""
        try:
            # Try to parse as JSON
            if response.strip().startswith('{'):
                improvements = json.loads(response)
            else:
                # If not JSON, extract content manually
                improvements = self._extract_from_text(response)
            
            # Ensure required fields
            improvements.setdefault("improved_title", original_title)
            improvements.setdefault("improved_body", response)
            improvements.setdefault("labels", ["bug"] if issue_type == "bug" else ["feature", "story"])
            
            return improvements
            
        except json.JSONDecodeError:
            # Fallback: treat entire response as body
            return {
                "improved_title": original_title,
                "improved_body": response,
                "labels": ["bug"] if issue_type == "bug" else ["feature", "story"]
            }
    
    def _extract_from_text(self, response: str) -> Dict[str, Any]:
        """Extract structured data from text response."""
        lines = response.split('\n')
        improvements = {}
        
        for line in lines:
            if line.strip().startswith("Improved Title:"):
                improvements["improved_title"] = line.replace("Improved Title:", "").strip()
            elif line.strip().startswith("Title:"):
                improvements["improved_title"] = line.replace("Title:", "").strip()
            elif line.strip().startswith("Improved Body:"):
                improvements["improved_body"] = line.replace("Improved Body:", "").strip()
            elif line.strip().startswith("Body:"):
                improvements["improved_body"] = line.replace("Body:", "").strip()
        
        if "improved_body" not in improvements:
            improvements["improved_body"] = response
            
        return improvements

def main():
    """Main function for GitHub Actions."""
    
    # Get environment variables
    repo_name = os.getenv("REPO_NAME")
    issue_number = int(os.getenv("ISSUE_NUMBER", "0"))
    
    if not repo_name or issue_number == 0:
        logger.error("Missing required environment variables")
        return False
    
    # Initialize QAPilot
    qapilot = QAPilotOllama()
    
    # Improve the issue
    success = qapilot.improve_issue_with_ollama(repo_name, issue_number)
    
    if success:
        logger.info("Issue improvement completed successfully")
    else:
        logger.error("Failed to improve issue")
    
    return success

if __name__ == "__main__":
    main()
