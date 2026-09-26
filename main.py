import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
from pydantic import SecretStr
from pathlib import Path
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
# Import your custom module
from external_mcp_servers import MultiMCPModuleManager

load_dotenv(verbose=False)
user_prompt = input("Ask your agent> ")

@tool
def get_time_now():
    """
        This would display current time
    """
    now = datetime.now()
    return now

# Define your server layout
SERVER_CONFIGURATIONS = {
    "weather": {
            "transport": "stdio",
            "command": "python",
            "args": [str(Path("./mcp_servers/Weather-MCP-ClaudeDesktop/main.py").resolve())]
        }
}

local_tools = [get_time_now]

async def run_agent():
    # 1. Instantiate the module manager
    mcp_module = MultiMCPModuleManager(SERVER_CONFIGURATIONS)
    
    # 2. Extract the consolidated tools
    mcp_tools = await mcp_module.async_load_tools()
    all_tools = local_tools + mcp_tools
    print(f"Successfully imported {len(mcp_tools)} MCP and {len(local_tools)} local tools from the MCP module.")

    # 3. Initialize your LangGraph agent
    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=SecretStr(os.getenv("GOOGLE_API_KEY")),
    )
    agent = create_agent(model, all_tools)

    # 4. Invoke the agent
    result = await agent.ainvoke(
        {
            "messages": [
            {
                "role": "user",
                "content": user_prompt
            }]
        }
    )
    print("\nAgent Output:", result["messages"][-1].text)

if __name__ == "__main__":
    asyncio.run(run_agent())
