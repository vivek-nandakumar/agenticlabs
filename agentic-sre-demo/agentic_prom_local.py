import os
import sys
import asyncio
import re
import httpx

# 1️⃣  Add the `libs` directory from your clone to PYTHONPATH
sys.path.insert(0, os.path.join(os.getcwd(), "agno", "libs"))

# 2️⃣  Now import from the local AGNO source tree
from agno.agent.agent import Agent
from agno.tools.tool import Tool
from agno.mcp.client import MCPClient
from agno.llm.openai import OpenAI

async def main():
    # 3️⃣  Register a Prometheus tool via MCP
    mcp = MCPClient()
    mcp.register_tool(
        name="prometheus_query",
        url="http://localhost:9090/api/v1/query",
        method="GET",
        query_param="query",
        description="Run a PromQL query against local Prometheus",
    )

    # 4️⃣  Wrap it in AGNO’s generic Tool abstraction
    prom_tool = Tool(
        name="prometheus_query",
        description=mcp.get_tool("prometheus_query").description,
        func=lambda q: httpx.get(
            mcp.get_tool("prometheus_query").url,
            params={"query": q}
        ).json()
    )

    # 5️⃣  Build the Agent with your single tool
    agent = Agent(
        name="sre_agent",
        tools=[prom_tool],
        llm=OpenAI(model="gpt-4o-mini", temperature=0.0)
    )

    # 6️⃣  Run a query
    answer = await agent.run(
        "What is the up value for localhost? Use the prometheus_query tool."
    )
    print("Agent says:", answer)

if __name__ == "__main__":
    asyncio.run(main())
