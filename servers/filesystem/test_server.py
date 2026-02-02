"""Tests for the Filesystem MCP Server."""

import tempfile
from pathlib import Path

import pytest

# Import server functions for testing
from server import (
    get_allowed_directories,
    get_mime_type,
    is_allowed_path,
    is_supported_file,
    load_config,
    should_ignore,
)


class TestConfig:
    """Tests for configuration loading."""

    def test_load_config_returns_dict(self):
        """Config should return a dictionary."""
        config = load_config()
        assert isinstance(config, dict)

    def test_config_has_required_keys(self):
        """Config should have required keys."""
        config = load_config()
        assert "allowed_directories" in config
        assert "ignore_patterns" in config
        assert "supported_extensions" in config


class TestPathValidation:
    """Tests for path validation functions."""

    def test_should_ignore_node_modules(self):
        """Should ignore node_modules directories."""
        path = Path("/home/user/project/node_modules/package/index.js")
        assert should_ignore(path) is True

    def test_should_ignore_git_directory(self):
        """Should ignore .git directories."""
        path = Path("/home/user/project/.git/config")
        assert should_ignore(path) is True

    def test_should_ignore_pycache(self):
        """Should ignore __pycache__ directories."""
        path = Path("/home/user/project/__pycache__/module.cpython-311.pyc")
        assert should_ignore(path) is True

    def test_should_not_ignore_regular_file(self):
        """Should not ignore regular Python files."""
        path = Path("/home/user/project/main.py")
        assert should_ignore(path) is False


class TestFileTypeDetection:
    """Tests for file type detection."""

    def test_python_file_supported(self):
        """Python files should be supported."""
        path = Path("/home/user/project/main.py")
        assert is_supported_file(path) is True

    def test_markdown_file_supported(self):
        """Markdown files should be supported."""
        path = Path("/home/user/project/README.md")
        assert is_supported_file(path) is True

    def test_binary_file_not_supported(self):
        """Binary files should not be supported."""
        path = Path("/home/user/project/image.png")
        assert is_supported_file(path) is False

    def test_get_mime_type_python(self):
        """Python files should have correct MIME type."""
        path = Path("/home/user/project/main.py")
        assert get_mime_type(path) == "text/x-python"

    def test_get_mime_type_json(self):
        """JSON files should have correct MIME type."""
        path = Path("/home/user/project/config.json")
        assert get_mime_type(path) == "application/json"

    def test_get_mime_type_unknown(self):
        """Unknown files should return text/plain."""
        path = Path("/home/user/project/file.xyz")
        assert get_mime_type(path) == "text/plain"


class TestIntegration:
    """Integration tests with actual files."""

    def test_list_directory_with_temp_files(self):
        """Test listing a directory with temporary files."""
        # This would require setting up allowed_directories in config
        # and creating temporary files. Skipped for basic setup.
        pass

    def test_search_files_with_temp_files(self):
        """Test searching files with temporary files."""
        # This would require setting up allowed_directories in config
        # and creating temporary files. Skipped for basic setup.
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
