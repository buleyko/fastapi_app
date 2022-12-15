from sqlalchemy import create_engine
from .model import Base
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)
from app.config import cfg 


engine = create_engine(
    cfg.database_url,
    connect_args={'check_same_thread': False},
    echo=True
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base(cls=Base)