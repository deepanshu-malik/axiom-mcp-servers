"""Abstract base class for MCP servers."""

from abc import ABC, abstractmethod
from typing import Any


class BaseMCPServer(ABC):
    """Abstract base class for all MCP server implementations."""

    @abstractmethod
    async def list_resources(self) -> list[Any]:
        """List all available resources."""
        pass

    @abstractmethod
    async def read_resource(self, uri: str) -> str:
        """Read a specific resource by URI."""
        pass

    @abstractmethod
    async def list_tools(self) -> list[Any]:
        """List available tools."""
        pass

    @abstractmethod
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Call a tool with given arguments."""
        pass
