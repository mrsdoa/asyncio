import asyncio
import aiohttp
import requests
from database import save_to_db


SW_API = 'https://swapi.dev/api/people/'

async def get_hero(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


def name_generator(url_list):
    try:
        for url in url_list:
            req = requests.get(url)
            yield req.json()['name']
    except KeyError:
        for url in url_list:
            req = requests.get(url)
            yield req.json()['title']


async def get_homeworld_name(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_sw_heroes():
    sw_persons_list = list()
    persons_tasks = [get_hero(f'{SW_API}/{i}') for i in range(1, 83)]
    persons_info = await asyncio.gather(*persons_tasks)
    for person in persons_info:
        if person != {'detail': 'Not found'}:
            hero_data = dict()
            hero_data['birth_year'] = person['birth_year']
            hero_data['eye_color'] = person['eye_color']
            hero_data['films'] = ', '.join(name_generator(person['films']))
            hero_data['gender'] = person['gender']
            hero_data['hair_color'] = person['hair_color']
            hero_data['height'] = person['height']
            planet = await get_homeworld_name(person['homeworld'])
            hero_data['homeworld'] = planet['name']
            hero_data['mass'] = person['mass']
            hero_data['name'] = person['name']
            hero_data['skin_color'] = person['skin_color']
            hero_data['species'] = ', '.join(name_generator(person['species']))
            hero_data['starships'] = ', '.join(name_generator(person['starships']))
            hero_data['vehicles'] = ', '.join(name_generator(person['vehicles']))
            sw_persons_list.append(hero_data)
    return list(sw_persons_list)


async def main():
    list_charact = await get_sw_heroes()
    await save_to_db(list_charact)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
