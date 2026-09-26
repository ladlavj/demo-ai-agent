import asyncio
import os
import subprocess
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import weather_mcp

load_dotenv(verbose=False)
user_prompt = input("Ask your agent> ")

def get_weather(city: str) -> str:
    '''
        get weather for given city
    '''
    return f"The weather in {city} is sunny with a high of 25°C."


agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are weather answering assistant"
)


result = agent.invoke(
    {
        "messages": [
        {
            "role": "user",
            "content": user_prompt
        }]
    }
)

def main():
    # print("AI Agent initializing...")
    # Add your agent initialization here
    # print(f"GEMINI_API_KEY loaded: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
#    print(result["messages"][-1].text)
    print(asyncio.run(weather_mcp.get_openweather(user_prompt)))

if __name__ == "__main__":
    main()
