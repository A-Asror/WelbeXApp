import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as column, relationship
from geoalchemy2.types import Geometry
from geoalchemy2.shape import from_shape
from shapely import Point

from src.utils.exceptions.database import EntityDoesNotExist
from src.repository.table import Base

__all__ = ['LocationTable']


# class CountryTable(Base):
#     __tablename__ = "country"
#
#     title: SQLAlchemyMapped[str] = column(sa.String(length=400), nullable=False, unique=True)
#     description: SQLAlchemyMapped[str] = column(sa.String(length=7000))
#     states: SQLAlchemyMapped[list['StateTable']] = relationship("StateTable", backref="country")
#
#     mapper_args = {"eager_defaults": True}
#
#
# class StateTable(Base):  # Таблица штатов
#     __tablename__ = 'state'
#
#     title: SQLAlchemyMapped[str] = column(sa.String(length=400), nullable=False, unique=True)
#     city: SQLAlchemyMapped[str] = column(sa.String(length=400), nullable=False)
#     description: SQLAlchemyMapped[str] = column(sa.Text, nullable=True)
#     country_id: SQLAlchemyMapped[int] = column(
#         sa.Integer, sa.ForeignKey("country.id", ondelete="RESTRICT"), nullable=False
#     )
#     cities: SQLAlchemyMapped[list['CityTable']] = relationship("CityTable", backref="state")
#
#     mapper_args = {"eager_defaults": True}


class LocationTable(Base):
    __tablename__ = 'location'

    country: SQLAlchemyMapped[str] = column(sa.String(length=400), nullable=False)
    state: SQLAlchemyMapped[str] = column(sa.String(length=400), nullable=False)
    city: SQLAlchemyMapped[str] = column(sa.String(length=400), nullable=False)
    post_code: SQLAlchemyMapped[str] = column(sa.String(length=15), nullable=False)
    location: SQLAlchemyMapped[Geometry] = column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=True), nullable=False
    )
    lat: SQLAlchemyMapped[float] = column(sa.Numeric(scale=6), nullable=False)
    lng: SQLAlchemyMapped[float] = column(sa.Numeric(scale=6), nullable=False)

    mapper_args = {"eager_defaults": True}

    def __init__(self, country: str, state: str, city: str, post_code: str, lat: float, lng: float, **kwargs):
        super().__init__(**kwargs)
        self.country = country  # type: ignore
        self.state = state  # type: ignore
        self.city = city  # type: ignore
        self.post_code = post_code  # type: ignore
        self.lat = lat  # type: ignore
        self.lng = lng  # type: ignore
        self.location = from_shape(Point(lng, lat))

    @classmethod
    async def get_location_by_post_code(cls, db_async_session: AsyncSession, post_code: str):
        stmt = sa.select(LocationTable.lat, LocationTable.lng).where(LocationTable.post_code == post_code)
        query = await db_async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f'Postcode with `{post_code}` does not exist!')

        post_code: LocationTable = query.fetchone()  # type: ignore

        return post_code

    @classmethod
    async def get_count(cls, session: AsyncSession) -> int:
        query = await session.execute(sa.select(sa.func.count(LocationTable.id)))
        return query.scalar_one()


# class PostCodeTable(Base):
#     __tablename__ = "location"
#
#     city_id: SQLAlchemyMapped[int] = column(sa.Integer, sa.ForeignKey("city.id", ondelete="RESTRICT"), nullable=False)
#     post_code: SQLAlchemyMapped[str] = column(sa.String(length=15), nullable=False)
#     location: SQLAlchemyMapped[Geometry] = column(
#         Geometry(geometry_type='POINT', srid=4326, spatial_index=True), nullable=False
#     )
#     lat: SQLAlchemyMapped[float] = column(sa.Numeric(scale=4), nullable=False)
#     lng: SQLAlchemyMapped[float] = column(sa.Numeric(scale=4), nullable=False)
#
#     mapper_args = {"eager_defaults": True}

    # @classmethod
    # async def get_location_by_post_code(cls, db_async_session: AsyncSession, post_code: str):
    #     stmt = sa.select([PostCodeTable.lat, PostCodeTable.lng]).where(PostCodeTable.post_code == post_code)
    #     query = await db_async_session.execute(statement=stmt)
    #
    #     if not query:
    #         raise EntityDoesNotExist(f'Postcode with `{post_code}` does not exist!')
    #
    #     post_code: PostCodeTable = query.scalar()
    #
    #     return post_code
