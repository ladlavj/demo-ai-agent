# mcp_manager.py
import asyncio
from typing import List, Dict, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool

class MultiMCPModuleManager:
    """
    A Python module wrapper for managing multiple MCP servers
    and exposing their aggregated tools to LangChain agents.
    """
    def __init__(self, server_configs: Dict[str, Dict[str, Any]]):
        """
        Initializes the client with a dictionary of server configs.

        Example config:
        {
            "weather": {"transport": "http", "url": "http://localhost:8000/mcp"},
            "db": {"transport": "stdio", "command": "python", "args": ["db_server.py"]}
        }
        """
        self.client = MultiServerMCPClient(server_configs)
        self._tools: List[BaseTool] = []

    async def async_load_tools(self) -> List[BaseTool]:
        """Asynchronously fetches and compiles tools from all active servers."""
        if not self._tools:
            self._tools = await self.client.get_tools()
        return self._tools

    def load_tools_sync(self) -> List[BaseTool]:
        """Synchronously fetches tools (useful if your agent setup isn't fully async)."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # If an async loop is already running, you should await async_load_tools instead
            raise RuntimeError("Async loop running. Use 'await async_load_tools()' instead.")

        return asyncio.run(self.async_load_tools())