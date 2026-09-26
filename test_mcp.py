import asyncio
from pathlib import Path
from langchain.mcp import MCPAdapter
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

async def main():
    path = Path("../Weather-MCP-ClaudeDesktop/main.py").resolve()
    print("Resolved path:", path)
    
    async with MCPAdapter(path) as adapter:
        tools = await adapter.list_tools()
        print("Tools:", tools)
        agent = create_agent("gemini-3.5-flash-lite", tools)
        result = await agent.ainvoke({"messages": [{"role": "user", "content": "What is the weather in London?"}]})
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
