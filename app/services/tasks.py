import asyncio

async def reverse_stream(data: str):
    result = ""
    for ch in data[::-1]:
        result += ch
        await asyncio.sleep(0.2)
        yield result

async def uppercase_stream(data: str):
    result = ""
    for ch in data:
        result += ch.upper()
        await asyncio.sleep(0.2)
        yield result

async def count_stream(data: str):
    count = 0
    for _ in data:
        count += 1
        await asyncio.sleep(0.2)
        yield f"count: {count}"

async def delay_stream(data: str):
    for i in range(5):
        await asyncio.sleep(1)
        yield f"processing step {i+1} for {data}"
