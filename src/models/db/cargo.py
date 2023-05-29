import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as column
from geoalchemy2 import WKTElement
from geoalchemy2.types import Geometry
from shapely import Point
from geoalchemy2.shape import from_shape

from src.repository.table import Base


__all__ = ['CargoTable']


class CargoTable(Base):
    __tablename__ = 'cargo'

    pick_up_lat: SQLAlchemyMapped[float] = column(sa.Numeric(scale=6), nullable=False)
    pick_up_lng: SQLAlchemyMapped[float] = column(sa.Numeric(scale=6), nullable=False)
    pick_up_post_code: SQLAlchemyMapped[str] = column(sa.String(length=15), nullable=False)
    pick_up: SQLAlchemyMapped[WKTElement] = column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=True), nullable=False
    )
    delivery_lat: SQLAlchemyMapped[float] = column(sa.Numeric(scale=6), nullable=False)
    delivery_lng: SQLAlchemyMapped[float] = column(sa.Numeric(scale=6), nullable=False)
    delivery_post_code: SQLAlchemyMapped[str] = column(sa.String(length=15), nullable=False)
    delivery: SQLAlchemyMapped[WKTElement] = column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=True), nullable=False
    )
    weight: SQLAlchemyMapped[float] = column(sa.Numeric(scale=3), nullable=False)
    description: SQLAlchemyMapped[str] = column(sa.Text, nullable=False)

    mapper_args = {"eager_defaults": True}
    __table_args__ = (sa.PrimaryKeyConstraint('id'),)

    def __init__(
        self,
        pick_up_post_code: SQLAlchemyMapped[str],
        pick_up_lat: SQLAlchemyMapped[float],
        pick_up_lng: SQLAlchemyMapped[float],
        delivery_post_code: SQLAlchemyMapped[str],
        delivery_lat: SQLAlchemyMapped[float],
        delivery_lng: SQLAlchemyMapped[float],
        weight: float,
        description: str,
        **kwargs
    ):
        super(CargoTable, self).__init__(**kwargs)
        self.pick_up_lng = pick_up_lng
        self.pick_up_lat = pick_up_lat
        self.pick_up_post_code = pick_up_post_code
        self.pick_up = from_shape(Point(pick_up_lng, pick_up_lat), srid=4326)
        self.delivery_lng = delivery_lng
        self.delivery_lat = delivery_lat
        self.delivery_post_code = delivery_post_code
        self.delivery = from_shape(Point(delivery_lng, delivery_lat), srid=4326)
        self.weight = weight  # type: ignore
        self.description = description   # type: ignore

    async def update(self, payload: dict) -> 'CargoTable':
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)

        return self


    # def filter_by_radius(self, stmt: sa.Select, radius: int, center_point: [float, float]):
    #     stmt = stmt.where(
    #         sa.func.distance(
    #             self.pick_up_lat, self.pick_up_lng, self.delivery_lat, self.delivery_lng
    #         )
    #         < radius
    #     )
    #     stmt = stmt.where(
    #         sa.func.distance(
    #             self.pick_up_lat, self.pick_up_lng, center_point[0], center_point[1]
    #         )
    #         < radius
    #     )
    #     return stmt
