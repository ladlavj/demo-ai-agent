import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
import asyncio
import os

# Import modules to test
from src.main import SERVER_CONFIGURATIONS, get_agent, run_agent
from src.tools.local_tools import get_time_now

class TestAgentComponents(unittest.IsolatedAsyncioTestCase):
    
    def test_get_time_now(self):
        """Test that get_time_now tool returns a valid datetime object."""
        # Using .invoke to call the LangChain tool
        result = get_time_now.invoke({})
        self.assertIsInstance(result, datetime)
        
    def test_server_configurations(self):
        """Test that SERVER_CONFIGURATIONS is properly defined for MCP."""
        self.assertIn("weather", SERVER_CONFIGURATIONS)
        self.assertIn("command", SERVER_CONFIGURATIONS["weather"])
        self.assertEqual(SERVER_CONFIGURATIONS["weather"]["command"], "python")

    @patch("src.main.MultiMCPModuleManager")
    @patch("src.main.create_agent")
    async def test_get_agent(self, mock_create_agent, mock_mcp_manager):
        """Test get_agent initializes correctly without hitting real APIs."""
        # Setup mocks
        mock_mcp_instance = MagicMock()
        mock_mcp_instance.async_load_tools = AsyncMock(return_value=[MagicMock()])
        mock_mcp_manager.return_value = mock_mcp_instance
        
        mock_agent_instance = MagicMock()
        mock_create_agent.return_value = mock_agent_instance
        
        # We need GOOGLE_API_KEY so the SecretStr validation doesn't fail
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
            agent = await get_agent()
            
        self.assertEqual(agent, mock_agent_instance)
        mock_mcp_manager.assert_called_once_with(SERVER_CONFIGURATIONS)
        mock_mcp_instance.async_load_tools.assert_called_once()
        mock_create_agent.assert_called_once()

    @patch("src.main.get_agent")
    @patch("builtins.input", side_effect=["test prompt", "exit"])
    @patch("builtins.print")
    async def test_run_agent_chat_mode(self, mock_print, mock_input, mock_get_agent):
        """Test run_agent in chat mode loops and exits cleanly."""
        mock_agent = MagicMock()
        
        # Create a fake message object that has a 'content' attribute to mimic AIMessage
        fake_msg = MagicMock()
        fake_msg.content = "agent response"
        fake_msg.text = "agent response" # Just in case it checks .text
        
        mock_agent.ainvoke = AsyncMock(return_value={
            "messages": [fake_msg]
        })
        mock_get_agent.return_value = mock_agent
        
        await run_agent(chat_mode=True)
        
        # Verify input was called twice (once for "test prompt", once for "exit")
        self.assertEqual(mock_input.call_count, 2)
        mock_agent.ainvoke.assert_called_once()

    @patch("src.main.get_agent")
    @patch("builtins.input", return_value="one time prompt")
    @patch("builtins.print")
    async def test_run_agent_single_mode(self, mock_print, mock_input, mock_get_agent):
        """Test run_agent in single execution mode."""
        mock_agent = MagicMock()
        
        fake_msg = MagicMock()
        fake_msg.content = "single response"
        fake_msg.text = "single response"
        
        mock_agent.ainvoke = AsyncMock(return_value={
            "messages": [fake_msg]
        })
        mock_get_agent.return_value = mock_agent
        
        await run_agent(chat_mode=False)
        
        mock_input.assert_called_once_with("Ask your agent> ")
        mock_agent.ainvoke.assert_called_once()

if __name__ == '__main__':
    unittest.main()
