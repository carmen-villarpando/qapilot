"""Main issue improvement logic."""

import logging
import re
from typing import Any

from github_client import GitHubClient
from enhanced_template_engine import EnhancedTemplateEngine

logger = logging.getLogger(__name__)


class IssueImprover:
    """Main class for improving GitHub issues."""

    def __init__(self, github_client: GitHubClient, template_engine: EnhancedTemplateEngine):
        """Initialize issue improver."""
        self.github_client = github_client
        self.template_engine = template_engine

    async def improve_issue_from_comment(
        self,
        repo_name: str,
        issue_number: int,
        comment_body: str,
        comment_author: str
    ) -> bool:
        """Improve issue triggered by comment."""
        # Check if comment contains the trigger command
        if not self._is_improve_command(comment_body):
            logger.info(f"Comment does not contain improve command: {comment_body}")
            return False

        # Get the issue
        issue = self.github_client.get_issue(repo_name, issue_number)
        if not issue:
            logger.error(f"Could not find issue {issue_number} in {repo_name}")
            return False

        title = issue.title
        logger.info(f"Improving issue {issue_number}: '{title}'")

        # Add reaction to indicate processing
        try:
            issue.create_reaction("+1")
        except Exception as e:
            logger.warning(f"Could not add reaction: {e}")

        # Get repository context
        repo_context = await self._get_repo_context(repo_name)

        # Generate improvements using templates with app terminology
        improvements = self.template_engine.improve_issue(title, repo_context, repo_name)
        if not improvements:
            logger.error("Failed to generate improvements")
            await self._add_error_comment(repo_name, issue_number)
            return False

        # Apply improvements
        success = await self._apply_improvements(repo_name, issue_number, improvements)

        if success:
            await self._add_success_comment(repo_name, issue_number, comment_author)
        else:
            await self._add_error_comment(repo_name, issue_number)

        return success

    async def improve_issue_from_creation(
        self,
        repo_name: str,
        issue_number: int,
        issue_body: str,
        issue_author: str
    ) -> bool:
        """Improve issue triggered on creation."""
        # Check if issue body contains the trigger command
        if not self._is_improve_command(issue_body):
            logger.info(f"Issue body does not contain improve command: {issue_body}")
            return False

        # Get the issue
        issue = self.github_client.get_issue(repo_name, issue_number)
        if not issue:
            logger.error(f"Could not find issue {issue_number} in {repo_name}")
            return False

        title = issue.title
        logger.info(f"Improving issue {issue_number} on creation: '{title}'")

        # Add reaction to indicate processing
        try:
            issue.create_reaction("+1")
        except Exception as e:
            logger.warning(f"Could not add reaction: {e}")

        # Get repository context
        repo_context = await self._get_repo_context(repo_name)

        # Generate improvements using templates with app terminology
        improvements = self.template_engine.improve_issue(title, repo_context, repo_name)
        if not improvements:
            logger.error("Failed to generate improvements")
            await self._add_error_comment(repo_name, issue_number)
            return False

        # Apply improvements
        success = await self._apply_improvements(repo_name, issue_number, improvements)

        if success:
            await self._add_creation_success_comment(repo_name, issue_number, issue_author)
        else:
            await self._add_error_comment(repo_name, issue_number)

        return success

    def _is_improve_command(self, comment_body: str) -> bool:
        """Check if comment contains the improve command."""
        # Look for /improve-issue command
        return bool(re.search(r'/improve-issue', comment_body, re.IGNORECASE))

    async def _get_repo_context(self, repo_name: str) -> str:
        """Get repository context for better suggestions."""
        try:
            repo = self.github_client.github.get_repo(repo_name)

            # Get basic repo info
            context = f"Repository: {repo_name}\n"
            context += f"Description: {repo.description or 'No description'}\n"
            context += f"Language: {repo.language or 'Unknown'}\n"

            # Get available labels
            labels = self.github_client.get_repo_labels(repo_name)
            if labels:
                context += f"Available labels: {', '.join(labels[:20])}\n"

            return context
        except Exception as e:
            logger.warning(f"Could not get repo context: {e}")
            return ""

    async def _apply_improvements(
        self,
        repo_name: str,
        issue_number: int,
        improvements: dict[str, Any]
    ) -> bool:
        """Apply improvements to the issue."""
        try:
            # Build improved body
            current_issue = self.github_client.get_issue(repo_name, issue_number)
            if not current_issue:
                return False

            new_body = self._build_improved_body(current_issue.body or "", improvements)

            # Extract labels
            labels = []
            if improvements.get("labels"):
                if isinstance(improvements["labels"], list):
                    labels = improvements["labels"]
                else:
                    labels = [label.strip() for label in improvements["labels"].split(",")]
                labels = [label for label in labels if label]  # Remove empty

            # Update issue
            success = self.github_client.update_issue(
                repo_name=repo_name,
                issue_number=issue_number,
                body=new_body,
                labels=labels
            )

            return success
        except Exception as e:
            logger.error(f"Error applying improvements: {e}")
            return False

    def _build_improved_body(self, current_body: str, improvements: dict[str, Any]) -> str:
        """Build improved issue body."""
        # Clean /improve-issue command from current body
        cleaned_body = re.sub(r'/improve-issue', '', current_body, flags=re.IGNORECASE).strip()
        
        # Use the complete improved description from EnhancedTemplateEngine
        if improvements.get("description"):
            improved_description = improvements['description']
            
            # Add QAPilot signature if not already present
            if "QAPilot improved this issue" not in improved_description:
                improved_description += "\n\n---\n\n*QAPilot improved this issue*"
            
            # Combine with cleaned original body if there's meaningful content
            if cleaned_body and len(cleaned_body.strip()) > 10:
                return f"{cleaned_body}\n\n---\n\n{improved_description}"
            else:
                return improved_description
        else:
            # Fallback to original behavior if no description
            return cleaned_body

    async def _add_success_comment(
        self,
        repo_name: str,
        issue_number: int,
        triggered_by: str
    ) -> None:
        """Add success comment."""
        comment = "🚀 **Issue improved by QAPilot!**\n\n"
        comment += f"Triggered by @{triggered_by}\n"
        comment += "Added description, reproduction steps, expected behavior, and labels."

        self.github_client.add_comment(repo_name, issue_number, comment)

    async def _add_creation_success_comment(
        self,
        repo_name: str,
        issue_number: int,
        created_by: str
    ) -> None:
        """Add success comment for issue creation."""
        comment = "🚀 **Issue automatically improved by QAPilot!**\n\n"
        comment += f"Created by @{created_by}\n"
        comment += "Automatically added description, reproduction steps, expected behavior, and labels."

        self.github_client.add_comment(repo_name, issue_number, comment)

    async def _add_error_comment(self, repo_name: str, issue_number: int) -> None:
        """Add error comment."""
        comment = "❌ **QAPilot Error**\n\n"
        comment += "Sorry, I couldn't improve this issue. Please check the logs and try again."

        self.github_client.add_comment(repo_name, issue_number, comment)

    @staticmethod
    def from_env() -> "IssueImprover":
        """Create IssueImprover from environment variables."""
        github_client = GitHubClient.from_env()
        template_engine = EnhancedTemplateEngine()
        return IssueImprover(github_client, template_engine)
