import typing

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from src.repository.database import async_db


__all__ = ['get_async_session', 'async_repository']


async def get_async_session() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
    try:
        yield async_db.async_session
    except Exception as e:
        print(e)
        await async_db.async_session.rollback()
    finally:
        await async_db.async_session.close()


async def async_repository():  # For individual requests outside the scope of FastAP
    async_session = sessionmaker(  # type: ignore
        async_db.async_engine, class_=SQLAlchemyAsyncSession, expire_on_commit=False, autoflush=False
    )
    return async_session
