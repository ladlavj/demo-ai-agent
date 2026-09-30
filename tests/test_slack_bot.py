import unittest
from unittest.mock import patch, MagicMock, AsyncMock

# Import the handlers
from src.slack_bot import (
    handle_app_mention_events,
    handle_direct_message,
    handle_agent_command,
    handle_button_click,
    ask_agent
)

class TestSlackBot(unittest.TestCase):
    
    @patch("src.slack_bot.ask_agent")
    def test_handle_app_mention_events(self, mock_ask_agent):
        """Test that the bot responds to @mentions by querying the AI."""
        mock_ask_agent.return_value = "Mocked AI Response"
        
        mock_say = MagicMock()
        mock_body = {"event": {"text": "<@U123> what is the weather?"}}
        
        handle_app_mention_events(mock_body, mock_say)
        
        # Verify it said "thinking" and then the response
        self.assertEqual(mock_say.call_count, 2)
        mock_say.assert_any_call("Let me think about that...")
        mock_say.assert_any_call("Mocked AI Response")
        mock_ask_agent.assert_called_once_with("<@U123> what is the weather?")

    @patch("src.slack_bot.ask_agent")
    def test_handle_direct_message(self, mock_ask_agent):
        """Test that the bot responds to direct messages."""
        mock_ask_agent.return_value = "DM Response"
        
        mock_say = MagicMock()
        mock_message = {"channel_type": "im", "text": "hello"}
        
        handle_direct_message(mock_message, mock_say)
        
        mock_say.assert_called_once_with("DM Response")
        mock_ask_agent.assert_called_once_with("hello")
        
    @patch("src.slack_bot.ask_agent")
    def test_handle_direct_message_ignores_public(self, mock_ask_agent):
        """Ensure the bot ignores non-im messages in the generic message handler."""
        mock_say = MagicMock()
        mock_message = {"channel_type": "channel", "text": "hello"}
        
        handle_direct_message(mock_message, mock_say)
        
        mock_say.assert_not_called()
        mock_ask_agent.assert_not_called()

    @patch("src.slack_bot.ask_agent")
    def test_handle_agent_command(self, mock_ask_agent):
        """Test the slash command /ask-agent."""
        mock_ask_agent.return_value = "Command Response"
        
        mock_ack = MagicMock()
        mock_respond = MagicMock()
        mock_command = {"text": "do something"}
        
        handle_agent_command(mock_ack, mock_respond, mock_command)
        
        mock_ack.assert_called_once()
        self.assertEqual(mock_respond.call_count, 2)
        mock_respond.assert_any_call("Querying AI for: 'do something'...")
        mock_respond.assert_any_call("Command Response")
        mock_ask_agent.assert_called_once_with("do something")

    def test_handle_button_click(self):
        """Test the button click interactive action."""
        mock_ack = MagicMock()
        mock_say = MagicMock()
        
        handle_button_click(mock_ack, {}, mock_say)
        
        mock_ack.assert_called_once()
        mock_say.assert_called_once_with("Button clicked! I can trigger a specific AI workflow now.")

    @patch("src.slack_bot.get_agent_sync")
    def test_ask_agent_helper(self, mock_get_agent_sync):
        """Test the ask_agent helper that bridges async LangGraph with sync Slack Bolt."""
        mock_agent = MagicMock()
        fake_msg = MagicMock()
        fake_msg.content = "AI reply"
        fake_msg.text = "AI reply" # Set explicitly so getattr(last_msg, 'text') works
        
        # We need to mock ainvoke which is an async function in LangChain
        mock_agent.ainvoke = AsyncMock(return_value={"messages": [fake_msg]})
        mock_get_agent_sync.return_value = mock_agent
        
        result = ask_agent("hello")
        
        self.assertEqual(result, "AI reply")
        mock_agent.ainvoke.assert_called_once()

if __name__ == '__main__':
    unittest.main()
