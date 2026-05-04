import asyncio
from app.services.agent import GeminiAgent

async def reverse_stream(data: dict):
    result = ""
    for ch in data["query"][::-1]:
        result += ch
        await asyncio.sleep(0.2)
        yield result

async def uppercase_stream(data: dict):
    result = ""
    for ch in data["query"]:
        result += ch.upper()
        await asyncio.sleep(0.2)
        yield result

async def count_stream(data: dict):
    count = 0
    for _ in data["query"]:
        count += 1
        await asyncio.sleep(0.2)
        yield f"count: {count}"

async def delay_stream(data: dict):
    for i in range(5):
        await asyncio.sleep(1)
        yield f"processing step {i+1} for {data}"

async def agent_task(data : dict):
    agent = GeminiAgent()
    async for step in agent.run(
        query = data["query"],
        max_steps = data.get("max_steps", 5)
    ):
        yield step