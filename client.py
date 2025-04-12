import aiohttp
from asyncio import run

async def main():

    async with aiohttp.ClientSession() as session:
        response = await session.get('http://127.0.0.1:8080/')
        print(response.status)
        print(await response.text())

run(main())