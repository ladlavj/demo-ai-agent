import asyncio
from pathlib import Path
from langchain.mcp import MCPAdapter
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI


async def get_openweather(prompt: str):
    '''
        Fetches the weather for provided city from the Openweather MCP tool running locally as STDIO
    '''
    server_path = Path("../Weather-MCP-ClaudeDesktop/main.py").resolve()
    try:
        async with MCPAdapter(server_path) as adapter:
            tools = await adapter.list_tools()
            
            # Using ChatGoogleGenerativeAI directly to avoid VertexAI setup requirements
            # Assuming "gemini-1.5-flash" or you can change to your specific model
            llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
            agent = create_agent(llm, tools)
            
            response = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
            print("\nResponse:")
            # Note: the output of ainvoke is typically a dictionary containing 'messages'
            # We print the content of the last message (the AI's response)
            return response["messages"][-1].text
    except Exception as e:
        return f"\nError running MCP server or agent: {e}"

