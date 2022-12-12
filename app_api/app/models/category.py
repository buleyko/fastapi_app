from app.vendors.base.database import Base
from sqlalchemy.orm import (
	relationship,
	backref,
)
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
)
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	JSON,
)


class Category(ValidMixin, TimestampsMixin, Base):
	__tablename__ = 'categories'

	name = Column(
		JSON,
		default = {'def':''}
	)
	short_desc = Column(
		JSON,
		default = {'def':''}
	)
	parent_id = Column(
		Integer, 
		ForeignKey('categories.id'),
		nullable=True,
	)
	children = relationship(
		'Category', 
		backref=backref('parent', remote_side='Category.id')
	)
	articles = relationship(
		'Article', 
		back_populates='category'
	)