from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession


class BaseCRUDRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.async_session = async_session

    async def paginate(self, statement: Select, page: int = 1, page_size: int = 15):
        stmt = statement.limit(page_size).offset((page -1) * page_size)
        return await self.async_session.execute(statement=stmt)
