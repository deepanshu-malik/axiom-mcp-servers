# Axiom MCP Servers

MCP (Model Context Protocol) server implementations for Axiom personal knowledge assistant.

## Servers

### Filesystem Server

Exposes local files through the MCP protocol.

**Features:**
- List files in allowed directories
- Read file contents
- Search files by name/content

**Usage:**
```bash
cd servers/filesystem
python server.py
```

### GitHub Server

Access GitHub repositories through MCP.

**Features:**
- List configured repositories
- Read files from repos
- Search code in repos

**Usage:**
```bash
cd servers/github
python server.py
```

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"
```

## Testing

```bash
# Test with MCP inspector
mcp-inspector python servers/filesystem/server.py
```

## Configuration

Each server has its own `config.yaml` file. See the individual server directories for configuration options.
