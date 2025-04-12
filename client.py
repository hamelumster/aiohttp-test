import aiohttp
from asyncio import run

async def main():

    async with aiohttp.ClientSession() as session:
        response = await session.post('http://127.0.0.1:8080/hello/world')
        print(response.status)
        print(await response.json())

run(main())