"""Filesystem MCP Server - Exposes local files through MCP protocol.

This server provides:
- Resources: List and read files from allowed directories
- Tools: Search files by name or content

Usage:
    python server.py

Test with MCP inspector:
    mcp-inspector python server.py
"""

import fnmatch
import os
from pathlib import Path
from typing import Any

import yaml
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP(
    name="filesystem",
    instructions="Access local files from configured directories. "
    "Use list_directory to browse, read_file to get contents, "
    "and search_files to find files by pattern or content.",
)

# Configuration
CONFIG_PATH = Path(__file__).parent / "config.yaml"
_config: dict[str, Any] | None = None


def load_config() -> dict[str, Any]:
    """Load server configuration from config.yaml."""
    global _config
    if _config is None:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH) as f:
                _config = yaml.safe_load(f)
        else:
            _config = {
                "allowed_directories": ["~/Documents", "~/projects"],
                "ignore_patterns": [
                    "*/node_modules/*",
                    "*/.git/*",
                    "*/__pycache__/*",
                    "*.pyc",
                    "*/.env",
                    "*/venv/*",
                    "*/.venv/*",
                ],
                "supported_extensions": [
                    ".py", ".md", ".txt", ".js", ".ts",
                    ".json", ".yaml", ".yml", ".html", ".css",
                    ".sh", ".toml", ".rst", ".ini", ".cfg",
                ],
            }
    return _config


def get_allowed_directories() -> list[Path]:
    """Get list of allowed directories as resolved paths."""
    config = load_config()
    dirs = []
    for d in config.get("allowed_directories", []):
        path = Path(d).expanduser().resolve()
        if path.exists() and path.is_dir():
            dirs.append(path)
    return dirs


def is_allowed_path(path: Path) -> bool:
    """Check if a path is within allowed directories."""
    resolved = path.resolve()
    allowed_dirs = get_allowed_directories()
    return any(
        resolved == allowed or resolved.is_relative_to(allowed)
        for allowed in allowed_dirs
    )


def should_ignore(path: Path) -> bool:
    """Check if a path matches any ignore patterns."""
    config = load_config()
    path_str = str(path)
    for pattern in config.get("ignore_patterns", []):
        if fnmatch.fnmatch(path_str, pattern):
            return True
    return False


def is_supported_file(path: Path) -> bool:
    """Check if file has a supported extension."""
    config = load_config()
    supported = config.get("supported_extensions", [])
    return path.suffix.lower() in supported


def get_mime_type(path: Path) -> str:
    """Get MIME type for a file."""
    mime_types = {
        ".py": "text/x-python",
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".js": "text/javascript",
        ".ts": "text/typescript",
        ".json": "application/json",
        ".yaml": "text/yaml",
        ".yml": "text/yaml",
        ".html": "text/html",
        ".css": "text/css",
        ".sh": "text/x-shellscript",
        ".toml": "text/x-toml",
        ".rst": "text/x-rst",
        ".ini": "text/plain",
        ".cfg": "text/plain",
    }
    return mime_types.get(path.suffix.lower(), "text/plain")


# ============================================================================
# MCP Resources
# ============================================================================


@mcp.resource("file:///{path}")
def read_file_resource(path: str) -> str:
    """Read a file by its path.

    Args:
        path: Absolute path to the file

    Returns:
        File contents as string
    """
    file_path = Path("/" + path).resolve()

    if not is_allowed_path(file_path):
        raise ValueError(f"Access denied: {file_path} is not in allowed directories")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    if should_ignore(file_path):
        raise ValueError(f"Access denied: {file_path} matches ignore pattern")

    return file_path.read_text(encoding="utf-8", errors="replace")


# ============================================================================
# MCP Tools
# ============================================================================


@mcp.tool()
def list_allowed_directories() -> list[dict[str, str]]:
    """List all directories that are configured for access.

    Returns:
        List of allowed directories with their paths
    """
    dirs = get_allowed_directories()
    return [{"path": str(d), "exists": d.exists()} for d in dirs]


@mcp.tool()
def list_directory(
    directory: str,
    recursive: bool = False,
    max_depth: int = 3,
) -> list[dict[str, Any]]:
    """List files in a directory.

    Args:
        directory: Path to directory (can use ~ for home)
        recursive: Whether to list recursively
        max_depth: Maximum depth for recursive listing (default 3)

    Returns:
        List of files with metadata
    """
    dir_path = Path(directory).expanduser().resolve()

    if not is_allowed_path(dir_path):
        raise ValueError(f"Access denied: {dir_path} is not in allowed directories")

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")

    if not dir_path.is_dir():
        raise ValueError(f"Not a directory: {dir_path}")

    files = []

    def scan_directory(path: Path, current_depth: int = 0):
        if current_depth > max_depth:
            return

        try:
            for item in sorted(path.iterdir()):
                if should_ignore(item):
                    continue

                relative_path = item.relative_to(dir_path)

                if item.is_file() and is_supported_file(item):
                    try:
                        stat = item.stat()
                        files.append({
                            "name": item.name,
                            "path": str(item),
                            "relative_path": str(relative_path),
                            "type": "file",
                            "size": stat.st_size,
                            "extension": item.suffix,
                            "mime_type": get_mime_type(item),
                        })
                    except OSError:
                        pass

                elif item.is_dir() and recursive:
                    files.append({
                        "name": item.name,
                        "path": str(item),
                        "relative_path": str(relative_path),
                        "type": "directory",
                    })
                    scan_directory(item, current_depth + 1)

                elif item.is_dir() and not recursive:
                    files.append({
                        "name": item.name,
                        "path": str(item),
                        "relative_path": str(relative_path),
                        "type": "directory",
                    })

        except PermissionError:
            pass

    scan_directory(dir_path)
    return files


@mcp.tool()
def read_file(file_path: str) -> dict[str, Any]:
    """Read contents of a file.

    Args:
        file_path: Path to file (can use ~ for home)

    Returns:
        Dictionary with file content and metadata
    """
    path = Path(file_path).expanduser().resolve()

    if not is_allowed_path(path):
        raise ValueError(f"Access denied: {path} is not in allowed directories")

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"Not a file: {path}")

    if should_ignore(path):
        raise ValueError(f"Access denied: {path} matches ignore pattern")

    if not is_supported_file(path):
        raise ValueError(
            f"Unsupported file type: {path.suffix}. "
            f"Supported: {load_config().get('supported_extensions', [])}"
        )

    stat = path.stat()
    content = path.read_text(encoding="utf-8", errors="replace")

    return {
        "path": str(path),
        "name": path.name,
        "content": content,
        "size": stat.st_size,
        "lines": len(content.splitlines()),
        "extension": path.suffix,
        "mime_type": get_mime_type(path),
    }


@mcp.tool()
def search_files(
    pattern: str,
    directory: str | None = None,
    content_search: str | None = None,
    max_results: int = 50,
) -> list[dict[str, Any]]:
    """Search for files by name pattern and/or content.

    Args:
        pattern: Glob pattern to match file names (e.g., "*.py", "test_*.py")
        directory: Directory to search in (searches all allowed dirs if not specified)
        content_search: Optional string to search for within file contents
        max_results: Maximum number of results to return (default 50)

    Returns:
        List of matching files with metadata
    """
    results = []

    # Determine directories to search
    if directory:
        dir_path = Path(directory).expanduser().resolve()
        if not is_allowed_path(dir_path):
            raise ValueError(f"Access denied: {dir_path} is not in allowed directories")
        search_dirs = [dir_path]
    else:
        search_dirs = get_allowed_directories()

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        # Use rglob for recursive pattern matching
        try:
            for file_path in search_dir.rglob(pattern):
                if len(results) >= max_results:
                    break

                if not file_path.is_file():
                    continue

                if should_ignore(file_path):
                    continue

                if not is_supported_file(file_path):
                    continue

                # If content search is specified, check file contents
                if content_search:
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="replace")
                        if content_search.lower() not in content.lower():
                            continue

                        # Find matching lines
                        matching_lines = []
                        for i, line in enumerate(content.splitlines(), 1):
                            if content_search.lower() in line.lower():
                                matching_lines.append({
                                    "line_number": i,
                                    "content": line.strip()[:200],
                                })
                                if len(matching_lines) >= 5:
                                    break

                        results.append({
                            "path": str(file_path),
                            "name": file_path.name,
                            "extension": file_path.suffix,
                            "matches": matching_lines,
                        })

                    except (OSError, UnicodeDecodeError):
                        continue
                else:
                    try:
                        stat = file_path.stat()
                        results.append({
                            "path": str(file_path),
                            "name": file_path.name,
                            "extension": file_path.suffix,
                            "size": stat.st_size,
                        })
                    except OSError:
                        continue

        except PermissionError:
            continue

        if len(results) >= max_results:
            break

    return results


@mcp.tool()
def get_file_info(file_path: str) -> dict[str, Any]:
    """Get metadata about a file without reading its contents.

    Args:
        file_path: Path to file (can use ~ for home)

    Returns:
        Dictionary with file metadata
    """
    path = Path(file_path).expanduser().resolve()

    if not is_allowed_path(path):
        raise ValueError(f"Access denied: {path} is not in allowed directories")

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    stat = path.stat()

    return {
        "path": str(path),
        "name": path.name,
        "extension": path.suffix,
        "size": stat.st_size,
        "is_file": path.is_file(),
        "is_directory": path.is_dir(),
        "mime_type": get_mime_type(path) if path.is_file() else None,
        "is_supported": is_supported_file(path) if path.is_file() else None,
        "modified_time": stat.st_mtime,
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("Starting Filesystem MCP Server...")
    print(f"Config: {CONFIG_PATH}")
    print(f"Allowed directories: {[str(d) for d in get_allowed_directories()]}")
    print("\nRun with: mcp-inspector python server.py")
    print("Or add to your MCP client configuration.\n")

    mcp.run()
