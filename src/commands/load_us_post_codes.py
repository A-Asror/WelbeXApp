import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import pandas as pd
from pydantic import BaseModel, Field

from src.repository.database import async_db
from src.models import db


def csv_path() -> str:
    return os.path.dirname(__file__) + '/import_data/uszips.csv'
    # return os.path.dirname(__file__) + '/import_data/qwe.csv'


async def import_post_codes(session: AsyncSession, instances: list[db.LocationTable]):
    session.add_all(instances=instances)
    await session.commit()


class ImportUSZips(BaseModel):
    post_code: str = Field(..., alias='zip')
    lat: float
    lng: float
    city: str
    state: str = Field(..., alias='state_name')

    def location_instance(self):
        return db.LocationTable(
            country='US',
            state=self.state,
            city=self.city,
            post_code=self.post_code,
            lat=self.lat,
            lng=self.lng
        )

    @classmethod
    async def read_csv(cls, session: AsyncSession):
        num = 0
        instances = []
        csv = pd.read_csv(csv_path(), low_memory=False, dtype={'zip': str})

        for index, row in csv.iterrows():
            num += 1
            instance: db.LocationTable = cls(**row.to_dict()).location_instance()
            instances.append(instance)
            if num == 1000:
                await import_post_codes(session=session, instances=instances)
                num, instances = 0, []

        if instances:
            await import_post_codes(session=session, instances=instances)

    @classmethod
    def csv_read_columns(cls) -> list[str]:
        return list(cls.schema()['properties'].keys())


async def async_repository():
    async_session = sessionmaker(async_db.async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)  # type: ignore
    async with async_session() as session:
        await ImportUSZips.read_csv(session=session)  # type: ignore


async def run_command():
    await async_repository()


if __name__ == '__main__':
    asyncio.run(run_command())
