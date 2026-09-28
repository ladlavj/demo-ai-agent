# Common
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import os
from pydantic import SecretStr

# LLM
from langchain_google_genai import ChatGoogleGenerativeAI

# Tools
from langchain_mcp_adapters.client import MultiServerMCPClient

# Agent
from langchain.agents import create_agent

# Make Agent by linking LLM with Tool
load_dotenv(verbose=False)
all_tools = list()
mcp_server_path = Path("../Weather-MCP-ClaudeDesktop/main.py").resolve()

llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=SecretStr(os.getenv("GOOGLE_API_KEY"))
    )

server_configs = {
    "weather": {
        "transport": "stdio",
        "command": "python",
        "args": [str(mcp_server_path)]
    }
}

async def main():
    client = MultiServerMCPClient(server_configs)
    tools = await client.get_tools()
    agent = create_agent(
        model = llm,
        tools = list(tools),
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
