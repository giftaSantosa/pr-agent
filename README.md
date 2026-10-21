# pr-agent

An AI agent that reviews a GitHub pull request and drafts a comment. It only posts after you approve.

Built with Python and the Claude API.

## Features

- Reviews any PR by its number
- Reads other files in the repo when it needs more context
- Asks for your approval before posting
- Can only read files inside the repo

## Setup

1. Install:

   ```bash
   git clone https://github.com/giftaSantosa/pr-agent.git
   cd pr-agent
   python3 -m venv venv
   source venv/bin/activate
   pip install anthropic requests python-dotenv
   ```

2. Create a `.env` file in the `pr-agent` folder:

   ```
   ANTHROPIC_API_KEY=your-anthropic-key
   GITHUB_TOKEN=your-github-token
   GITHUB_OWNER=your-github-username
   GITHUB_REPO=repo-to-review
   ```

   - Get an Anthropic key at [console.anthropic.com](https://console.anthropic.com).
   - Create a GitHub fine-grained token with **Pull requests: Read and write** and **Contents: Read**.

## Usage

From inside the repo you want to review, on the PR's branch:

```bash
git checkout <pr-branch>
python3 path/to/pr-agent/pr-agent.py <PR number>
```

The agent prints a draft comment and asks `Post? (y/n)`. Answer `y` to post it.
