import asyncio
import aiohttp

from models import init_db, People, Session

from more_itertools import chunked

CHUNK_SIZE = 10

async def paste_to_db(people):
    async with Session() as session:
        people = [People(json=person) for person in people]
        session.add_all(people)
        await session.commit()

async def get_person(person_id, session):
    response = await session.get(f'https://swapi.dev/api/people//{person_id}/')
    json = await response.json()
    return json

async def main():
    await init_db()

    async with aiohttp.ClientSession() as session:
        for people_id_chunk in chunked(range(1, 100), CHUNK_SIZE):
            coros = []
            for people_id in people_id_chunk:
                coros.append(get_person(people_id, session))
            result = await asyncio.gather(*coros)
            await paste_to_db(result)


asyncio.run(main())