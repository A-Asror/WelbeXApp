from __future__ import absolute_import, unicode_literals

import random

import asyncio

import sqlalchemy as sa

from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db
from src.api.dependencies.session import async_repository

from .settings.celery import celery


class PredictTransformersPipelineTask(Task):
    """
    Abstraction of Celery's Task class to support loading transformers model.
    """

    task_name = ""
    model_name = ""
    abstract = True

    def __init__(self):
        super().__init__()
        self.pipeline = None

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


async def _update_transport_number_every_3_minutes():
    async_session_generator = await async_repository()
    async_session: AsyncSession = async_session_generator()

    async with async_session as session:
        count_cargo = await db.LocationTable.get_count(session=session)
        random_choice = random.sample(range(count_cargo), 20)
        locations_stmt = sa.select(db.LocationTable.lat, db.LocationTable.lng).filter(
            db.LocationTable.id.in_(random_choice))
        locations_query = await session.execute(statement=locations_stmt)
        locations_result: list[db.LocationTable] = locations_query.all()  # type: ignore

        transports_stmt = sa.select(db.TransportTable)
        transports_query = await session.execute(statement=transports_stmt)
        transports_result: list[db.TransportTable] = transports_query.scalars().all()  # type: ignore

        for index in range(0, 20):
            location = locations_result[index]
            transport = transports_result[index]
            setattr(transport, 'location_lat', location.lat)
            setattr(transport, 'location_lng', location.lng)

        await session.commit()


@celery.task(
    ignore_result=False,
    base=PredictTransformersPipelineTask,
    task_name='update_transport_number_every_3_minutes',
    name='tasks.update_transport_number_every_3_minutes',
    bind=True)
def update_transport_number_every_3_minutes(self):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop.create_task(_update_transport_number_every_3_minutes()))
