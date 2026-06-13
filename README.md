# QAPilot

🤖 **GitHub issue improvement tool using GitHub Models API**

QAPilot automatically enhances your GitHub issues by analyzing simple titles and generating comprehensive descriptions, labels, and metadata.

## Features

- 🚀 **Manual Trigger**: Comment `/improve-issue` on any issue
- 🧠 **Smart Analysis**: Uses GitHub Models API (free tier)
- 🏷️ **Auto-labeling**: Suggests relevant labels based on content
- 📝 **Structured Output**: Adds description, reproduction steps, expected behavior
- 🎯 **GitHub Native**: Works entirely within GitHub UI
- 💰 **Free**: Uses GitHub's free tier models

## Quick Start

1. **Setup GitHub Secrets**:
   ```bash
   GITHUB_TOKEN: <your-github-pat>
   GITHUB_MODELS_TOKEN: <your-github-models-token>
   ```

2. **Enable GitHub Actions** in your repository

3. **Use it**: Comment `/improve-issue` on any issue

## How it Works

1. User creates issue with simple title (e.g., "el scroll no funciona")
2. User comments `/improve-issue`
3. GitHub Action triggers QAPilot
4. AI analyzes title and repository context
5. Issue is automatically updated with:
   - Detailed description
   - Step-by-step reproduction steps
   - Expected behavior
   - Relevant labels
   - Priority level
   - Suggested assignee

## Development

### Setup with uv

```bash
# Clone and install
git clone <repo>
cd qapilot
uv sync --dev

# Run tests
uv run pytest

# Lint
uv run ruff check .
uv run mypy .
```

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
# Edit .env with your tokens
```

### Project Structure

```
qapilot/
├── app/
│   ├── github_client.py       # GitHub API client
│   ├── github_models_client.py # GitHub Models API client
│   ├── issue_improver.py      # Main improvement logic
│   ├── main_improve_issue.py  # GitHub Actions entry point
│   └── prompts/
│       └── improve_prompt.txt # AI prompt template
├── .github/workflows/
│   └── issue-improve.yml     # GitHub Action
├── plan/                      # Project plans
├── tests/                     # Test suite
├── pyproject.toml            # uv configuration
└── README.md
```

## Requirements

- Python 3.11+
- GitHub Personal Access Token
- GitHub Models API Token
- Repository with GitHub Actions enabled

## License

MIT License - see LICENSE file for details
