import datetime as dt

from typing import Any

from celery.schedules import crontab
from pydantic import BaseModel


class Beat(BaseModel):
    task: str
    schedule: Any
    args: list | tuple | None = None
    kwargs: dict | None = None

    def __init__(
        self,
        task: str,
        schedule: Any,
        args: list | dict | None = None,
        kwargs: dict | None = None,
    ):
        super().__init__(task=f'tasks.{task}', schedule=schedule, args=args, kwargs=kwargs)


class RegisterBeatSchedule(BaseModel):
    """
    Example: beat_name = Beat(task='task_name', schedule=crontab(...))
    """

    update_transport_number_every_3_minutes = Beat(
        task='update_transport_number_every_3_minutes',
        schedule=crontab(minute='*/3')
    )


def get_beat_schedules():
    return RegisterBeatSchedule().dict()
