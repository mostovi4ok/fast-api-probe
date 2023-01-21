from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import env

async_engine = create_async_engine(env.FAST_DB_ASYNC)

AsyncSessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(async_engine, expire_on_commit=False)

engine = create_engine(env.FAST_DB)

SessionFactory = sessionmaker(engine)
