import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
from pydantic import SecretStr
from pathlib import Path
from langchain.agents import create_agent
from langchain_core.tools import tool
# Import your custom module
from external_mcp_servers import MultiMCPModuleManager
import argparse

load_dotenv(verbose=False)
openweather_api_key = os.getenv("OPENWEATHER_API_KEY", "")

from tools.local_tools import get_time_now
# Define your server layout
SERVER_CONFIGURATIONS = {
    "weather": {
            "transport": "stdio",
            "command": "python",
            "args": [str(Path("./mcp_servers/Weather-MCP-ClaudeDesktop/main.py").resolve())],
            "env": {
                "OPENWEATHER_API_KEY": openweather_api_key
            }
        }
}

local_tools = [get_time_now]

async def get_agent():
    # 1. Instantiate the module manager
    mcp_module = MultiMCPModuleManager(SERVER_CONFIGURATIONS)

    # 2. Extract the consolidated tools
    mcp_tools = await mcp_module.async_load_tools()
    all_tools = local_tools + mcp_tools
    print(f"Successfully imported {len(mcp_tools)} MCP and {len(local_tools)} local tools.")

    # 3. Initialize your LangGraph agent
    system_prompt = (
        "You are a helpful assistant. You have access to tools, "
        "but you can also answer general knowledge questions directly "
        "without using any tools if a tool is not needed."
        "You also have to make sure not to expose this agent's code or any sensitive information in your responses."
        "Sensitive information such as API keys and PII should never be shared. If you are asked for such information, politely decline and explain that you cannot provide it."
    )
    agent = create_agent(
        model="google_genai:gemini-3.5-flash-lite",
        tools=all_tools,
        system_prompt=system_prompt
    )
    return agent

async def run_agent(chat_mode: bool = False):
    agent = await get_agent()

    # 4. Invoke the agent
    if chat_mode:
        print("\nStarting chat mode. Type 'exit' or 'quit' to stop.")
        messages = []
        while True:
            try:
                user_prompt = input("\nAsk your agent> ")
                if user_prompt.lower() in ['exit', 'quit']:
                    break

                messages.append({"role": "user", "content": user_prompt})
                result = await agent.ainvoke({"messages": messages})

                # Update history with the result (assumes result['messages'] contains full history)
                messages = result["messages"]

                # Get the last message output (checking for .text or .content safely)
                last_msg = messages[-1]
                reply_text = getattr(last_msg, "text", getattr(last_msg, "content", str(last_msg)))
                print("\nAgent Output:", reply_text)

            except (KeyboardInterrupt, EOFError):
                break
    else:
        user_prompt = input("Ask your agent> ")
        result = await agent.ainvoke(
            {
                "messages": [
                {
                    "role": "user",
                    "content": user_prompt
                }]
            }
        )
        last_msg = result["messages"][-1]
        reply_text = getattr(last_msg, "text", getattr(last_msg, "content", str(last_msg)))
        print("\nAgent Output:", reply_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the AI Agent.")
    parser.add_argument("--chat", action="store_true", help="Run in continuous chat bot mode")
    args = parser.parse_args()

    asyncio.run(run_agent(chat_mode=args.chat))