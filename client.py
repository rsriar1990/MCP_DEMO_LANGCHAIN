from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio
import sys

async def main():
    # Start the weather server first: uv run python weather.py
    client=MultiServerMCPClient(
        {
            "math":{
                "command":sys.executable,
                "args":["mathserver.py"],
                "transport":"stdio",
            },
            "weather":{
                "url":"http://localhost:8000/mcp",
                "transport":"streamable-http",
            }
        }
    )

    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="qwen/qwen3.6-27b")
    agent=create_react_agent(model,tools)

    math_response=await agent.ainvoke(
        {"messages":[
            {"role":"user","content":"What is (2+2)*3?"}
        ]}
    )
    print("math response:",math_response["messages"][-1].content)

    weather_response=await agent.ainvoke(
        {"messages":[
            {"role":"user","content":"What is the weather in Tokyo?"}
        ]}
    )
    print("weather response:",weather_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
