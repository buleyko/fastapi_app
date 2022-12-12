from sqlalchemy.orm import relationship
from app.vendors.base.database import Base
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
)


class Tag(Base):
	__tablename__ = 'tags'

	name = Column(
		String, 
		unique=True,
	)