# 🔌 MCP Demo with LangChain

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-green.svg)](https://python.langchain.com/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io/)

A demonstration project showcasing how to seamlessly connect **Model Context Protocol (MCP)** servers with **LangChain** agents and chains. This project demonstrates dynamic tool discovery, context loading, and extensible agentic workflows powered by the open MCP standard.

---

## 📌 Overview

The **Model Context Protocol (MCP)** is an open standard that enables LLM applications to securely interact with external data sources, local filesystems, APIs, and execution tools.

This repository demonstrates how to:
- Connect LangChain agents to external MCP servers (stdio & SSE transports).
- Automatically expose MCP server tools as native LangChain `StructuredTool` objects.
- Build flexible agentic workflows using LangChain and LLM providers (e.g., OpenAI, Groq, Anthropic).

---

## ✨ Features

- **Seamless Tool Conversion**: Converts MCP tools into LangChain-compatible tools out of the box.
- **Multi-Server Support**: Intersect and aggregate tools across multiple local or remote MCP servers.
- **Dynamic Context Loading**: Fetch prompts, tools, and resources dynamically without re-deploying agent logic.
- **Asynchronous Execution**: Fully supports `asyncio` for non-blocking tool calls and stream execution.
- **Environment Management**: Configurable via `.env` files for clean secret and API key handling.

---

## 🛠️ Project Structure

```text
MCP_DEMO_LANGCHAIN/
│
├── mcp_servers/         # Configuration or custom MCP server implementations
├── src/                 # Core source code
│   ├── client.py        # LangChain MCP client implementation
│   ├── agent.py         # LangChain Agent definition & execution loop
│   └── utils.py         # Helper utilities and environment loaders
│
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python**: Version 3.10 or higher
- **Node.js / npx** *(Optional)*: Required if you are running Node-based MCP servers (e.g., `@modelcontextprotocol/server-filesystem`).

### 1. Clone the Repository

```bash
git clone [https://github.com/rsriar1990/MCP_DEMO_LANGCHAIN.git](https://github.com/rsriar1990/MCP_DEMO_LANGCHAIN.git)
cd MCP_DEMO_LANGCHAIN
```

### 2. Create and Activate Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*Key dependencies include:*
- `langchain`
- `langchain-mcp-adapters`
- `mcp`
- `python-dotenv`
- `langchain-openai` / `langchain-groq` / `langchain-anthropic`

---

## ⚙️ Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Add your API keys to `.env`:
   ```env
   # LLM Provider API Keys
   GROQ_API_KEY=your_groq_api_key_here

   # MCP Server Settings (if applicable)
   MCP_SERVER_PATH=/path/to/your/mcp/server
   ```

---

## 💡 Usage Example

Below is a minimal snippet illustrating how to connect to an MCP server and run a LangChain agent using the exposed tools:

```python
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

async def main():
    # Initialize Multi-Server MCP Client
    async with MultiServerMCPClient(
        {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"],
                "transport": "stdio",
            }
        }
    ) as client:
        # Load tools provided by the MCP server
        tools = client.get_tools()

        # Initialize LLM & Prompt
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        prompt = hub.pull("hwchase17/react")

        # Create LangChain Agent
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # Run query
        response = await agent_executor.ainvoke(
            {"input": "List all files in the current data directory."}
        )
        print("Agent Response:", response["output"])

if __name__ == "__main__":
    asyncio.run(main())
```

---
