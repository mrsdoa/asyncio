import asyncio
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .env import DB_USER, DB_NAME, DB_PASSWORD

Base = declarative_base()
sw_db = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'

class StarWarPerson(Base):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)

async def save_to_db(data):
    engine = create_async_engine(sw_db, echo=True,)

    async with engine.begin() as db_con:
        await db_con.run_sync(Base.metadata.drop_all)
        await db_con.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            for item in data:
                person = StarWarPerson(
                    name=item['name'],
                    birth_year=item['birth_year'],
                    eye_color=item['eye_color'],
                    films=item['films'],
                    gender=item['gender'],
                    hair_color=item['hair_color'],
                    height=item['height'],
                    homeworld=item['homeworld'],
                    mass=item['mass'],
                    skin_color=item['skin_color'],
                    species=item['species'],
                    starships=item['starships'],
                    vehicles=item['vehicles'],
                )
                session.add(person)

        await session.commit()


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
