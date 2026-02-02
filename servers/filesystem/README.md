# Filesystem MCP Server

Exposes local files through the Model Context Protocol (MCP) for Axiom.

## Features

### Tools

| Tool | Description |
|------|-------------|
| `list_allowed_directories` | List configured directories |
| `list_directory` | List files in a directory (with optional recursion) |
| `read_file` | Read file contents with metadata |
| `search_files` | Search by filename pattern and/or content |
| `get_file_info` | Get file metadata without reading contents |

### Resources

| Resource URI | Description |
|--------------|-------------|
| `file:///{path}` | Read file contents by absolute path |

## Configuration

Edit `config.yaml` to configure access:

```yaml
allowed_directories:
  - ~/Documents
  - ~/projects

ignore_patterns:
  - "*/node_modules/*"
  - "*/.git/*"
  - "*/__pycache__/*"

supported_extensions:
  - .py
  - .md
  - .txt
  - .json
```

## Security

- **Allowed Directories**: Only files within configured directories are accessible
- **Ignore Patterns**: Files/directories matching patterns are excluded
- **Supported Extensions**: Only files with listed extensions are served
- **No Write Access**: This server is read-only

## Installation

```bash
cd axiom-mcp-servers

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -e .
```

## Usage

### Run the Server

```bash
cd servers/filesystem
python server.py
```

### Test with MCP Inspector

```bash
# Install mcp-inspector if not already installed
pip install mcp

# Run inspector
mcp-inspector python server.py
```

### Add to MCP Client

For Claude Desktop or other MCP clients, add to your configuration:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["/path/to/axiom-mcp-servers/servers/filesystem/server.py"]
    }
  }
}
```

## Example Tool Calls

### List Directory

```json
{
  "tool": "list_directory",
  "arguments": {
    "directory": "~/projects",
    "recursive": true,
    "max_depth": 2
  }
}
```

### Search Files

```json
{
  "tool": "search_files",
  "arguments": {
    "pattern": "*.py",
    "content_search": "def main",
    "max_results": 20
  }
}
```

### Read File

```json
{
  "tool": "read_file",
  "arguments": {
    "file_path": "~/projects/myapp/main.py"
  }
}
```
