import sqlalchemy as sa

from src.utils.formatters import miles_to_meters
from src.models import db
from src.models import schemas
from src.utils.exceptions.http import exc_404

from geoalchemy2.elements import WKTElement
# from geoalchemy2 import ST_DWithin
from shapely.geometry import Point

from geoalchemy2.shape import from_shape

from .base import BaseCRUDRepository

__all__ = ['CargoCRUDRepository']


class CargoCRUDRepository(BaseCRUDRepository):

    async def create_cargo(self, instance: schemas.CargoInCreateSchema) -> db.CargoTable:

        pick_up = await db.LocationTable.get_location_by_post_code(
            db_async_session=self.async_session, post_code=instance.pick_up
        )
        delivery = await db.LocationTable.get_location_by_post_code(
            db_async_session=self.async_session, post_code=instance.delivery
        )

        new_cargo = db.CargoTable(
            pick_up_lat=pick_up.lat,
            pick_up_lng=pick_up.lng,
            pick_up_post_code=instance.pick_up,  # type: ignore
            delivery_lat=delivery.lat,
            delivery_lng=delivery.lng,
            delivery_post_code=instance.delivery,  # type: ignore
            weight=instance.weight,
            description=instance.description
        )

        self.async_session.add(instance=new_cargo)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_cargo)
        return new_cargo

    async def delete_by_id(self, cargo_id: int) -> str:
        stmt = sa.select(db.CargoTable.id).where(db.CargoTable.id == cargo_id)
        query = await self.async_session.execute(statement=stmt)

        if query.fetchone() is None:
            raise await exc_404.http_404_exc_id_not_found_request(pk=cargo_id, table=db.CargoTable)

        stmt = sa.delete(table=db.CargoTable).where(db.CargoTable.id == cargo_id)
        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Cargo with id '{cargo_id}' is successfully deleted!"

    async def update_by_id(self, cargo_id: int, payload: schemas.CargoInUpdateSchema) -> db.CargoTable:

        stmt = sa.select(db.CargoTable).where(db.CargoTable.id == cargo_id)
        query = await self.async_session.execute(statement=stmt)
        cargo = query.scalar()

        if not cargo:
            raise await exc_404.http_404_exc_id_not_found_request(pk=cargo_id, table=db.CargoTable)

        update_stmt = sa.update(table=db.CargoTable).where(db.CargoTable.id == cargo_id)
        update_stmt = update_stmt.values(**payload.dict(exclude_defaults=True))

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=cargo)

        return cargo

    async def read_all_cargo(
        self,
        radius: int = 450,
        page_size: int = 15,
        page: int = 1,
    ):

        sub_query = sa.select(
            db.TransportTable.id,
            db.TransportTable.location,
        ).group_by(db.TransportTable.id, db.TransportTable.location).subquery()

        stmt = sa.select(
            db.CargoTable.id,
            db.CargoTable.pick_up_post_code,
            db.CargoTable.delivery_post_code,
            sa.func.count(sub_query.c.id).label('transports'),
        ).join(
            sub_query,
            sa.and_(sub_query.c.location.ST_DistanceSphere(db.CargoTable.pick_up) <= miles_to_meters(radius))
        ).group_by(db.CargoTable.id)

        query = await self.paginate(statement=stmt, page_size=page_size, page=page)

        return query.fetchall()

    async def read_by_id(self, cargo_id: int):

        stmt = sa.select(
            db.CargoTable.id,
            db.CargoTable.pick_up_post_code,
            db.CargoTable.delivery_post_code,
            db.CargoTable.pick_up_lat,
            db.CargoTable.pick_up_lng,
            db.CargoTable.weight,
            db.CargoTable.description
        ).where(db.CargoTable.id == cargo_id)
        query = await self.async_session.execute(statement=stmt)
        cargo = query.one_or_none()

        if not cargo:
            raise await exc_404.http_404_exc_id_not_found_request(pk=cargo_id, table=db.CargoTable)

        return cargo

    async def read_all_transports(self):
        stmt = sa.select(
            db.TransportTable.id,
            db.TransportTable.location_lng,
            db.TransportTable.location_lat,
            db.TransportTable.transport_number
        )
        query = await self.async_session.execute(statement=stmt)

        return query.fetchall()

    async def filter_by_radius_and_weight(
        self,
        radius: int,
        weight: int | None,
        page_size: int = 15,
        page: int = 1
    ):

        sub_query = sa.select(
            db.TransportTable.id,
            db.TransportTable.location,
        ).group_by(db.TransportTable.id, db.TransportTable.location).subquery()

        stmt = sa.select(
            db.CargoTable.id,
            db.CargoTable.pick_up_post_code,
            db.CargoTable.delivery_post_code,
            db.CargoTable.weight,
            sa.func.count(sub_query.c.id).label('transports'),
        ).group_by(db.CargoTable.id)

        if weight is not None:
            stmt = stmt.where(db.CargoTable.weight == weight)
        if radius is not None:
            stmt = stmt.join(
                sub_query,
                sub_query.c.location.ST_DistanceSphere(db.CargoTable.pick_up) >= miles_to_meters(radius)  # type: ignore
            )

        query = await self.paginate(statement=stmt, page_size=page_size, page=page)

        return query.fetchall()
