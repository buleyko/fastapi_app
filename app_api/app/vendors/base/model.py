from sqlalchemy.orm import declared_attr
from sqlalchemy import (
    Column,
    Integer,
)


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    # __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, primary_key=True, autoincrement=True)