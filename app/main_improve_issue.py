"""Main entry point for GitHub Actions to improve issues."""

import asyncio
import logging
import os
import sys

from issue_improver import IssueImprover
from template_engine import TemplateEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main function for GitHub Actions."""
    try:
        # Get environment variables
        repo_name = os.getenv("REPO_NAME")
        issue_number = int(os.getenv("ISSUE_NUMBER", "0"))
        comment_body = os.getenv("COMMENT_BODY", "")
        comment_author = os.getenv("COMMENT_AUTHOR", "")
        issue_body = os.getenv("ISSUE_BODY", "")
        issue_author = os.getenv("ISSUE_AUTHOR", "")

        logger.info(f"Processing issue {issue_number} in {repo_name}")
        
        # Check if this is a comment trigger or issue creation trigger
        if comment_body and comment_author:
            logger.info(f"Comment by {comment_author}: {comment_body[:100]}...")
            
            if not all([repo_name, issue_number, comment_body, comment_author]):
                logger.error("Missing required environment variables for comment")
                sys.exit(1)

            # Create improver and process comment
            improver = IssueImprover.from_env()
            success = await improver.improve_issue_from_comment(
                repo_name=repo_name,
                issue_number=issue_number,
                comment_body=comment_body,
                comment_author=comment_author
            )
        
        elif issue_body and issue_author:
            logger.info(f"Issue created by {issue_author}: {issue_body[:100]}...")
            
            if not all([repo_name, issue_number, issue_body, issue_author]):
                logger.error("Missing required environment variables for issue creation")
                sys.exit(1)

            # Create improver and process issue creation
            improver = IssueImprover.from_env()
            success = await improver.improve_issue_from_creation(
                repo_name=repo_name,
                issue_number=issue_number,
                issue_body=issue_body,
                issue_author=issue_author
            )
        
        else:
            logger.error("Neither comment nor issue creation data provided")
            sys.exit(1)

        if success:
            logger.info("Issue improved successfully")
            sys.exit(0)
        else:
            logger.error("Failed to improve issue")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
