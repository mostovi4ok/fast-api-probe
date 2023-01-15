import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async_engine = create_async_engine(os.environ["FAST_DB_ASYNC"])

engine = create_engine(os.environ["FAST_DB"])

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
