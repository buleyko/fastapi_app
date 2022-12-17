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


class TagItem(Base):
	__tablename__ = 'tags_items'

	tag_id = Column(
		Integer, 
	)
	item_key = Column(
		String(20), 
	) 
	item_id = Column(
		Integer, 
	)