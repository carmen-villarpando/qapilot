# QAPilot Hackathon Plan (English)

Create a GitHub issue improvement tool that uses GitHub's free models to automatically enhance ticket quality by analyzing simple titles and generating comprehensive descriptions, labels, and metadata when manually triggered by the user.

## Requirements Confirmed

1. **Trigger Mechanism**: Manual via GitHub UI comment (`/improve-issue`)
2. **Model**: GitHub Models API (free tier) - lowest resource consumption
3. **Scope**: Personal repositories only
4. **Output**: Direct ticket update after user finishes title update
5. **Interface**: 100% within GitHub UI, no external apps

## Market Research

Similar tools exist:
- **GitHub Copilot**: Auto-completes issues but requires paid subscription
- **Linear AI**: AI-powered issue management (separate platform)
- **Sentry Issues**: Auto-generates issue details (error-focused)
- **IssueOps**: GitHub Action for issue automation (limited AI)

**Our Differentiator**: Free, GitHub-native, uses GitHub's own models, manual trigger for user control.

## Implementation Plan

### Phase 1: Core Infrastructure
- Set up uv project structure with pyproject.toml
- Implement GitHub API client using PyGithub
- Create GitHub Models API client
- Design prompt templates for issue analysis
- Set up GitHub Actions workflow

### Phase 2: Manual Trigger System
- Implement comment-based trigger (`/improve-issue`)
- Create issue_comment event handler in GitHub Action
- Add permission checks and validation
- Build response mechanism in GitHub UI

### Phase 3: Business Logic
- Build issue_improver.py with GitHub Models integration
- Create structured output format (description, labels, priority, reproduction steps)
- Add error handling and user feedback
- Implement direct issue update after title change

### Phase 4: Integration & Testing
- Configure GitHub Models API secrets
- Add logging and monitoring
- Create test suite with mock data
- Deploy to personal repository

## Technical Stack
- **Package Manager**: uv
- **LLM**: GitHub Models API (free tier)
- **GitHub API**: PyGithub
- **Trigger**: Issue comment events
- **Deployment**: GitHub Actions (GitHub-hosted)

## User Workflow
1. User creates issue with simple title
2. User adds comment: `/improve-issue`
3. GitHub Action triggers, analyzes title with GitHub Models
4. Script updates issue with comprehensive details
5. User sees enhanced issue in same GitHub interface

## Success Criteria
- Manual trigger works via comment command
- GitHub Models API provides quality suggestions
- Direct issue updates without leaving GitHub
- Works on personal repositories
- Free tier usage stays within limits
