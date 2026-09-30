import os
import asyncio
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# 1. Import your AI Agent logic
from src.main import get_agent

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    token_verification_enabled=False
)

# --- Helper: Sync wrapper for your Async Agent ---
# We cache the agent so it only loads the tools once
global_agent = None

def get_agent_sync():
    global global_agent
    if global_agent is None:
        global_agent = asyncio.run(get_agent())
    return global_agent

def ask_agent(prompt: str) -> str:
    agent = get_agent_sync()
    # Provide the user prompt as history
    result = asyncio.run(agent.ainvoke({"messages": [{"role": "user", "content": prompt}]}))
    last_msg = result["messages"][-1]
    return getattr(last_msg, "text", getattr(last_msg, "content", str(last_msg)))


# --- USE CASE 1: @app.event ---
# Best for: Public channels. 
# Users ping the bot ("@Bot what's the weather?") and it replies in the channel.
@app.event("app_mention")
def handle_app_mention_events(body, say):
    # Extract the text the user sent
    text = body["event"]["text"]
    say("Let me think about that...") # Provide immediate feedback
    
    # Ask your agent and reply
    response = ask_agent(text)
    say(response)


# --- USE CASE 2: @app.message ---
# Best for: Direct Messages (DMs). 
# Users can just chat normally without needing to "@" mention the bot.
@app.message(".*") # Matches any text
def handle_direct_message(message, say):
    # We only want to reply to Direct Messages to avoid spamming public channels
    if message.get("channel_type") == "im":
        text = message.get("text")
        response = ask_agent(text)
        say(response)


# --- USE CASE 3: @app.command ---
# Best for: Silent or specific utility commands (e.g., "/ask-agent how is the weather?")
# The reply is only visible to the person who typed it (ephemeral).
@app.command("/ask-agent")
def handle_agent_command(ack, respond, command):
    ack() # You MUST acknowledge commands within 3 seconds
    text = command["text"]
    
    respond(f"Querying AI for: '{text}'...")
    response = ask_agent(text)
    respond(response) # 'respond' replies privately, 'say' replies publicly


# --- USE CASE 4: @app.action ---
# Best for: Interactive UI (Buttons, Dropdowns).
# If your agent sends a message with a button saying "Summarize this channel", 
# clicking it would trigger this function.
@app.action("button_click_id")
def handle_button_click(ack, body, say):
    ack()
    say("Button clicked! I can trigger a specific AI workflow now.")


# --- USE CASE 5: @app.shortcut ---
# Best for: Message context menus.
# A user clicks the "..." next to any Slack message and clicks your app's "Summarize" shortcut.
@app.shortcut("summarize_message")
def handle_shortcut(ack, shortcut, client):
    ack()
    # You could extract the message text from the shortcut payload, 
    # pass it to ask_agent("Summarize this: <text>"), and open a modal with the result!
    pass


# --- USE CASE 6: @app.view ---
# Best for: Modal Submissions.
# If a user fills out a complex form in Slack, hitting "Submit" triggers this.
@app.view("modal_submission_id")
def handle_view_submission(ack, body, view):
    ack()
    # Extract form data and feed it to the agent as structured context
    pass


if __name__ == "__main__":
    app_token = os.environ.get("SLACK_APP_TOKEN")
    if app_token:
        print("Starting AI Slack Bot...")
        SocketModeHandler(app, app_token).start()
    else:
        print("Please set SLACK_APP_TOKEN and SLACK_BOT_TOKEN environment variables.")
