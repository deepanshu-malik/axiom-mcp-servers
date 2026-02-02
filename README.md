# Axiom MCP Servers

MCP (Model Context Protocol) server implementations for Axiom personal knowledge assistant.

## Server Status

| Server | Status | Description |
|--------|--------|-------------|
| Filesystem | ✅ Complete | Local file access |
| GitHub | 🔲 Phase 6 | GitHub repository access |
| Google Drive | 🔲 Future | Google Drive access |

## Filesystem Server (Complete)

Full MCP server for local filesystem access using FastMCP.

### Features

**Tools:**
| Tool | Description |
|------|-------------|
| `list_allowed_directories` | Show configured directories |
| `list_directory` | Browse files with optional recursion |
| `read_file` | Get file contents with metadata |
| `search_files` | Find files by pattern and/or content |
| `get_file_info` | Get file metadata |

**Resources:**
| URI | Description |
|-----|-------------|
| `file:///{path}` | Read file by absolute path |

**Security:**
- Configurable allowed directories
- Ignore patterns (node_modules, .git, __pycache__, etc.)
- Supported extensions whitelist
- Read-only access only

### Quick Start

```bash
cd axiom-mcp-servers

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
cd servers/filesystem
python -m pytest test_server.py -v

# Start server
python server.py
```

### Configuration

Edit `servers/filesystem/config.yaml`:

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
  - .json
```

### Use with MCP Clients

Add to your MCP client configuration (e.g., Claude Desktop):

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

## GitHub Server (Phase 6)

Placeholder for GitHub repository access. Will be implemented in Phase 6.

**Planned Features:**
- List configured repositories
- Read files from repos
- Search code in repos
- Get repository tree structure

## Project Structure

```
axiom-mcp-servers/
├── shared/                    # Common utilities
│   ├── base_server.py         # Abstract base class
│   └── utils.py               # File type detection
│
├── servers/
│   ├── filesystem/            # ✅ Complete
│   │   ├── server.py          # MCP server implementation
│   │   ├── config.yaml        # Configuration
│   │   ├── test_server.py     # Unit tests
│   │   └── README.md          # Documentation
│   │
│   ├── github/                # 🔲 Phase 6
│   │   ├── server.py          # Placeholder
│   │   └── config.yaml        # Configuration
│   │
│   └── gdrive/                # 🔲 Future
│       └── README.md          # Placeholder
│
└── tests/
    └── integration/
```

## Related Projects

- [axiom-core](https://github.com/deepanshu-malik/axiom-core) - FastAPI backend
- [axiom-experiments](https://github.com/deepanshu-malik/axiom-experiments) - Model comparison notebooks

## License

MIT License
