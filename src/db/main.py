from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config

engine = create_async_engine(
    url = Config.DATABASE_URL,
    echo=True,
    connect_args={"ssl":True})

async def init_db(): #create a database connection, keep this connection for as long as our database is running
    async with engine.begin() as conn:
        from src.db.models import Book 

        await conn.run_sync(SQLModel.metadata.create_all)


from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

async def get_session()-> AsyncGenerator[AsyncSession, None]: #getsession is dependency
    
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
