# Common
from datetime import datetime
from dotenv import load_dotenv
import asyncio
from pathlib import Path

# LLM
from langchain_google_genai import ChatGoogleGenerativeAI

# Tools
from langchain_core.tools import tool
#from langchain.mcp import MCPAdapter
from langchain_mcp_adapters.client import MultiServerMCPClient

# Agent
from langchain.agents import create_agent

# Make Agent by linking LLM with Tool
load_dotenv(verbose=False)
all_tools = list()
llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite"
    )

# Local tools
@tool
def get_time_now():
    """
        This would display current time
    """
    now = datetime.now()
    return now

# MCP tools
openweather_server_path = Path("../Weather-MCP-ClaudeDesktop/main.py").resolve()
mcp_client = MultiServerMCPClient(
        {
            "weather": {
                "command": "python",
                "args": [str(openweather_server_path)],
                "transport": "stdio",
            }
        }
    )

async def main():
#    async with MCPAdapter(server_path) as adapter:
#        mcp_tools = await adapter.list_tools()
#        all_tools = [get_time_now] + list(mcp_tools)
    mcp_tools = await mcp_client.get_tools()
    all_tools = [get_time_now] + mcp_tools
    agent = create_agent(
        model = llm,
        tools = all_tools,
        system_prompt = "You are a AI assistant, providing assistance on asked queries"
    )

    user_prompt = input("Ask AI > ")
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        }
    )
    print(result["messages"][-1].text)

if __name__ == "__main__":
    asyncio.run(main())
#    print(ai_response["messages"][-1].text)
