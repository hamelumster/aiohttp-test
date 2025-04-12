import aiohttp
from asyncio import run

async def main():

    # Создание пользователя
    # async with aiohttp.ClientSession() as session:
    #     response = await session.post('http://127.0.0.1:8080/api/v1/users',
    #                                    json={"username": "user_1", "password": "1234"},
    #                                   )
    #     print(response.status)
    #     print(await response.json())


    # Просмотр пользователя
    # async with aiohttp.ClientSession() as session:
    #     response = await session.get('http://127.0.0.1:8080/api/v1/users/1')
    #     print(response.status)
    #     print(await response.json())


    # Создание объявления
    # async with aiohttp.ClientSession() as session:
    #     response = await session.post('http://127.0.0.1:8080/api/v1/announcements',
    #                                    json={"title": "title_2",
    #                                          "description": "description_2",
    #                                          "owner": 1}
    #                                    )
    #     print(response.status)
    #     print(await response.json())

    # Просмотр созданного объявления
    # async with aiohttp.ClientSession() as session:
    #     response = await session.get('http://127.0.0.1:8080/api/v1/announcements/1')
    #     print(response.status)
    #     print(await response.json())

    # Редактирование объявления
    # async with aiohttp.ClientSession() as session:
    #     response = await session.patch('http://127.0.0.1:8080/api/v1/announcements/1',
    #                                    json={"title": "title_10",
    #                                          "description": "description_100010101",
    #                                          "owner": 1}
    #                                    )
    #     print(response.status)
    #     print(await response.json())

    # Удаление объявления
    # async with aiohttp.ClientSession() as session:
    #     response = await session.delete('http://127.0.0.1:8080/api/v1/announcements/1')
    #     print(response.status)
    #     print(await response.json())

run(main())