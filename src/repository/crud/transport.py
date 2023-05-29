import sqlalchemy as sa

from src.models import db
from src.models import schemas
from src.utils.exceptions.database import EntityDoesNotExist

from .base import BaseCRUDRepository


class TransportCRUDRepository(BaseCRUDRepository):

    async def update_by_id(self, transport_id, payload: schemas.TransportInUpdateSchema) -> db.TransportTable:

        stmt = sa.select(db.TransportTable).where(db.TransportTable.id == transport_id)
        query = await self.async_session.execute(statement=stmt)
        transport = query.scalar()

        if not transport:
            raise EntityDoesNotExist(f"Transport with id `{transport_id}` does not exist!")

        location = await db.LocationTable.get_location_by_post_code(
            db_async_session=self.async_session, post_code=payload.post_code
        )

        update_stmt = sa.update(table=db.TransportTable).where(db.TransportTable.id == transport_id)
        update_stmt = update_stmt.values(location=location)

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=transport)

        return transport
