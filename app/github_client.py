"""GitHub API client for issue management."""

import logging
import os

from github import Github, GithubException
from github.Issue import Issue

logger = logging.getLogger(__name__)


class GitHubClient:
    """Client for interacting with GitHub API."""

    def __init__(self, token: str):
        """Initialize GitHub client with token."""
        self.github = Github(token)
        self.token = token

    def get_issue(self, repo_name: str, issue_number: int) -> Issue | None:
        """Get issue by repository and number."""
        try:
            repo = self.github.get_repo(repo_name)
            return repo.get_issue(issue_number)
        except GithubException as e:
            logger.error(f"Error getting issue {issue_number} from {repo_name}: {e}")
            return None

    def update_issue(
        self,
        repo_name: str,
        issue_number: int,
        title: str | None = None,
        body: str | None = None,
        labels: list | None = None
    ) -> bool:
        """Update issue with new content."""
        try:
            issue = self.get_issue(repo_name, issue_number)
            if not issue:
                return False

            if title:
                issue.edit(title=title)
            if body:
                issue.edit(body=body)
            if labels:
                # Remove existing labels and add new ones
                issue.remove_from_labels()
                issue.add_to_labels(*labels)

            logger.info(f"Successfully updated issue {issue_number} in {repo_name}")
            return True
        except GithubException as e:
            logger.error(f"Error updating issue {issue_number} in {repo_name}: {e}")
            return False

    def add_comment(self, repo_name: str, issue_number: int, comment: str) -> bool:
        """Add comment to issue."""
        try:
            issue = self.get_issue(repo_name, issue_number)
            if not issue:
                return False

            issue.create_comment(comment)
            logger.info(f"Successfully added comment to issue {issue_number} in {repo_name}")
            return True
        except GithubException as e:
            logger.error(f"Error adding comment to issue {issue_number} in {repo_name}: {e}")
            return False

    def get_repo_labels(self, repo_name: str) -> list[str]:
        """Get all available labels in repository."""
        try:
            repo = self.github.get_repo(repo_name)
            return [label.name for label in repo.get_labels()]
        except GithubException as e:
            logger.error(f"Error getting labels from {repo_name}: {e}")
            return []

    @staticmethod
    def from_env() -> "GitHubClient":
        """Create GitHub client from environment variables."""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        return GitHubClient(token)
