import sqlalchemy as sa

from src.models import db
from src.models import schemas
from src.utils.exceptions.database import EntityDoesNotExist

from .base import BaseCRUDRepository

__all__ = ['LocationCRUDRepository']


class LocationCRUDRepository(BaseCRUDRepository):

    async def import_post_codes(self, instances: list[db.LocationTable], **kwargs):
        self.async_session.add_all(instances=instances)
        await self.async_session.commit()
