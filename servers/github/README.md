# GitHub MCP Server

Access GitHub repositories through the MCP protocol for Axiom.

## Features

- **Resources**: List repos, read files from repositories
- **Tools**: Search code, get repository tree

## Configuration

Edit `config.yaml` to configure:

```yaml
github_token: ${GITHUB_TOKEN}

default_repos:
  - owner/repo-name

cache_enabled: true
cache_ttl_hours: 24
```

## Environment Variables

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

## Usage

```bash
# Start the server
python server.py

# Test with MCP inspector
mcp-inspector python server.py
```
