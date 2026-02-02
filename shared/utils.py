"""Utility functions for MCP servers."""

import mimetypes
from pathlib import Path

# File type detection
SUPPORTED_EXTENSIONS = {
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
}


def get_mime_type(file_path: Path) -> str:
    """Get MIME type for a file."""
    ext = file_path.suffix.lower()
    if ext in SUPPORTED_EXTENSIONS:
        return SUPPORTED_EXTENSIONS[ext]

    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type or "application/octet-stream"


def is_text_file(file_path: Path) -> bool:
    """Check if a file is a text file."""
    mime_type = get_mime_type(file_path)
    return mime_type.startswith("text/") or mime_type in [
        "application/json",
        "application/javascript",
    ]
