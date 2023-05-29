import random
import string
from typing import Any

import asyncio

import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.api.dependencies.session import async_repository
from src.models import db


def get_transport_number():
    number = random.randint(1000, 9999)
    letter = random.choice(string.ascii_uppercase)
    return f"{number}{letter}"


def get_payload_capacity():
    return random.randint(1, 1000 + 1)


async def get_random_location(session: AsyncSession):
    stmt = sa.select(
        db.LocationTable.location,
        db.LocationTable.lat,
        db.LocationTable.lng,
    ).order_by(sa.func.random()).limit(1)
    location = await session.execute(statement=stmt)
    return location.fetchone()


class LoadTransports(BaseModel):
    transport_number: str | None = None
    payload_capacity: int | None = None
    location_lat: int | None = None
    location_lng: int | None = None
    location: Any | None = None

    async def transport_instance(self, session):
        location = await get_random_location(session)
        self.transport_number = get_transport_number()
        self.payload_capacity = get_payload_capacity()
        self.location = location.location
        self.location_lat = location.lat
        self.location_lng = location.lng

        return db.TransportTable(**self.dict())

    @classmethod
    async def run_command(cls, session: AsyncSession):

        instances: list[db.TransportTable] = []

        for _ in range(1, 21):
            await cls().transport_instance(session=session)
            instances.append(await cls().transport_instance(session=session))

        session.add_all(instances=instances)
        await session.commit()


async def run_command():
    async_session_generator = await async_repository()
    async_session: AsyncSession = async_session_generator()
    async with async_session as session:
        await LoadTransports.run_command(session=session)  # type: ignore


if __name__ == '__main__':
    asyncio.run(run_command())
