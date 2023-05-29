import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as column
from geoalchemy2 import Geometry

from src.repository.table import Base

__all__ = ['TransportTable']


class TransportTable(Base):
    __tablename__ = 'transport'

    id: SQLAlchemyMapped[int] = column(sa.Integer, primary_key=True, autoincrement="auto")
    location_lng: SQLAlchemyMapped[float] = column(sa.Numeric(scale=6), nullable=False)
    location_lat: SQLAlchemyMapped[float] = column(sa.Numeric(scale=6), nullable=False)
    transport_number: SQLAlchemyMapped[str] = column(sa.String(length=5), nullable=False)
    location: SQLAlchemyMapped[Geometry] = column(Geometry(geometry_type="Point", srid=4326), nullable=False)
    payload_capacity: SQLAlchemyMapped[int] = column(sa.Integer, nullable=False)

    __mapper_args__ = {'eager_defaults': True}
