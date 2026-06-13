"""Tests for issue improver functionality."""

from unittest.mock import Mock, patch

import pytest

from app.github_client import GitHubClient
from app.github_models_client import GitHubModelsClient
from app.issue_improver import IssueImprover


@pytest.fixture
def mock_github_client():
    """Mock GitHub client."""
    client = Mock(spec=GitHubClient)
    return client


@pytest.fixture
def mock_models_client():
    """Mock GitHub Models client."""
    client = Mock(spec=GitHubModelsClient)
    return client


@pytest.fixture
def issue_improver(mock_github_client, mock_models_client):
    """Create issue improver with mocked clients."""
    return IssueImprover(mock_github_client, mock_models_client)


class TestIssueImprover:
    """Test cases for IssueImprover."""

    @pytest.mark.asyncio
    async def test_is_improve_command(self, issue_improver):
        """Test command detection."""
        assert issue_improver._is_improve_command("/improve-issue")
        assert issue_improver._is_improve_command("Please /improve-issue now")
        assert issue_improver._is_improve_command("/IMPROVE-ISSUE")
        assert not issue_improver._is_improve_command("improve this issue")
        assert not issue_improver._is_improve_command("/other-command")

    def test_build_improved_body(self, issue_improver):
        """Test building improved issue body."""
        improvements = {
            "description": "The scroll is broken",
            "reproduction_steps": "1. Go to page\n2. Try to scroll",
            "expected_behavior": "Should scroll smoothly",
            "priority": "high",
            "assignee_suggestion": "dev-user"
        }

        result = issue_improver._build_improved_body("", improvements)

        assert "## 📝 Description" in result
        assert "## 🔧 Reproduction Steps" in result
        assert "## ✅ Expected Behavior" in result
        assert "## 📊 Metadata" in result
        assert "The scroll is broken" in result
        assert "**Priority:** high" in result

    @pytest.mark.asyncio
    async def test_improve_issue_from_comment_success(
        self, issue_improver, mock_github_client, mock_models_client
    ):
        """Test successful issue improvement."""
        # Mock issue
        mock_issue = Mock()
        mock_issue.title = "scroll not working"
        mock_issue.body = "Original body"
        mock_issue.create_reaction.return_value = None
        mock_issue.create_comment.return_value = None

        mock_github_client.get_issue.return_value = mock_issue
        mock_github_client.update_issue.return_value = True
        mock_github_client.add_comment.return_value = True
        mock_github_client.get_repo_labels.return_value = ["bug", "ui"]

        # Mock models response
        improvements = {
            "description": "Detailed description",
            "reproduction_steps": "1. Step 1\n2. Step 2",
            "expected_behavior": "Expected result",
            "labels": "bug,ui",
            "priority": "medium",
            "assignee_suggestion": "dev-user"
        }

        mock_models_client.improve_issue.return_value = improvements

        # Test
        result = await issue_improver.improve_issue_from_comment(
            repo_name="test/repo",
            issue_number=1,
            comment_body="/improve-issue",
            comment_author="testuser"
        )

        assert result is True
        mock_models_client.improve_issue.assert_called_once()
        mock_github_client.update_issue.assert_called_once()

    @pytest.mark.asyncio
    async def test_improve_issue_from_comment_no_command(
        self, issue_improver, mock_github_client, mock_models_client
    ):
        """Test issue improvement without command."""
        result = await issue_improver.improve_issue_from_comment(
            repo_name="test/repo",
            issue_number=1,
            comment_body="regular comment",
            comment_author="testuser"
        )

        assert result is False
        mock_models_client.improve_issue.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_repo_context(self, issue_improver, mock_github_client):
        """Test repository context gathering."""
        # Mock repo
        mock_repo = Mock()
        mock_repo.description = "Test repo"
        mock_repo.language = "Python"

        # Mock the github attribute
        mock_github_client.github = Mock()
        mock_github_client.github.get_repo.return_value = mock_repo
        mock_github_client.get_repo_labels.return_value = ["bug", "feature", "docs"]

        context = await issue_improver._get_repo_context("test/repo")

        assert "Repository: test/repo" in context
        assert "Description: Test repo" in context
        assert "Language: Python" in context
        assert "bug, feature, docs" in context


class TestGitHubModelsClient:
    """Test cases for GitHub Models client."""

    @pytest.mark.asyncio
    async def test_improve_issue_success(self):
        """Test successful issue improvement."""
        with patch('app.github_models_client.httpx.AsyncClient') as mock_client:
            # Mock response
            mock_response = Mock()
            mock_response.json.return_value = {
                "choices": [{"message": {"content": '{"description": "test"}'}}]
            }
            mock_response.raise_for_status.return_value = None

            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response

            client = GitHubModelsClient("test-token")
            result = await client.improve_issue("test title")

            assert result == {"description": "test"}

    def test_build_improve_prompt(self):
        """Test prompt building."""
        client = GitHubModelsClient("test-token")
        prompt = client._build_improve_prompt("test title", "repo context")

        assert "test title" in prompt
        assert "repo context" in prompt
        assert "JSON format" in prompt
