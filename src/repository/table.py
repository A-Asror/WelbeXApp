import datetime as dt
import typing

import sqlalchemy

from sqlalchemy.orm import DeclarativeBase, Mapped as SQLAlchemyMapped, mapped_column as column


class DBTable(DeclarativeBase):
    metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()  # type: ignore


class Base(DBTable):
    __abstract__ = True

    id: SQLAlchemyMapped[int] = column(sqlalchemy.Integer, primary_key=True, autoincrement="auto")
    created_at: SQLAlchemyMapped[dt.datetime] = column(sqlalchemy.DateTime(timezone=True), default=dt.datetime.utcnow)
    updated_at: SQLAlchemyMapped[dt.datetime] = column(
        sqlalchemy.DateTime(timezone=True), default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow
    )

    @classmethod
    def get_alembic_base_declarative(cls) -> typing.Type[DeclarativeBase]:
        return DBTable

# Base: typing.Type[DeclarativeBase] = DBTable
