# Filesystem MCP Server

Exposes local files through the MCP protocol for Axiom.

## Features

- **Resources**: List and read files from allowed directories
- **Tools**: Search files by name or content

## Configuration

Edit `config.yaml` to configure:

```yaml
allowed_directories:
  - ~/Documents
  - ~/projects

ignore_patterns:
  - "*/node_modules/*"
  - "*/.git/*"

supported_extensions:
  - .py
  - .md
  - .txt
```

## Usage

```bash
# Start the server
python server.py

# Test with MCP inspector
mcp-inspector python server.py
```

## Security

- Only files in `allowed_directories` are accessible
- Files matching `ignore_patterns` are excluded
- Only files with `supported_extensions` are served
