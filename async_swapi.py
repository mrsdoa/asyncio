import asyncio

from models import *
import aiohttp
import asyncpg
import more_itertools
from more_itertools import chunked

async def get_person(person_id, session):
    response = await session.get(f'https://swapi.dev/api/people/{person_id}')
    json = await response.json()
    if 'name' in json:
        print(json['name'])
        return [(json['birth_year'], json['eye_color'], " ".join(json['films']),
                  json['gender'], json['hair_color'], json['height'], json['homeworld'],
                  json['mass'], json['name'], json['skin_color'], " ".join(json['species']),
                  " ".join(json['starships']), " ".join(json['vehicles']))]
    else:
        return [('-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-')]



async def get_people(people_ids):
    tasks = [asyncio.create_task(get_person(person_id)) for person_id in people_ids]
    for task in tasks:
        tasks_result = await task
        yield tasks_result

async def insert_users(pool: asyncpg.Pool, people):
    query = 'INSERT INTO users (birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, ' \
            'skin_color, species, starships, vehicles) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, people)

async def main():
    pool = await asyncpg.create_pool(engine, min_size=20, max_size=20)

    for person_ids_chunk in more_itertools.chunked(range(1, 100), 10):
        coros = []
        async for person in get_people(person_ids_chunk):
            coros.append(asyncio.create_task(insert_users(pool, person)))

    await asyncio.gather(*coros)
    await pool.close()

asyncio.run(main())