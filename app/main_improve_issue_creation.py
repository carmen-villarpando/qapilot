"""Main entry point for GitHub Actions to improve issues on creation."""

import asyncio
import logging
import os
import sys

from issue_improver import IssueImprover

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
        issue_body = os.getenv("ISSUE_BODY", "")
        issue_author = os.getenv("ISSUE_AUTHOR", "")

        logger.info(f"Processing issue {issue_number} in {repo_name}")
        logger.info(f"Issue by {issue_author}: {issue_body[:100]}...")

        if not all([repo_name, issue_number, issue_body, issue_author]):
            logger.error("Missing required environment variables")
            sys.exit(1)

        # Create improver and process
        improver = IssueImprover.from_env()
        success = await improver.improve_issue_from_creation(
            repo_name=repo_name,
            issue_number=issue_number,
            issue_body=issue_body,
            issue_author=issue_author
        )

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
