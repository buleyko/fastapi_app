from app.vendors.base.database import Base
from sqlalchemy.orm import (
	relationship,
	backref,
)
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
	HelpersMixin,
)
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	Text,
	JSON,
)

class Media(ValidMixin, TimestampsMixin, Base):
	__tablename__ = 'medias'

	name = Column(
		String(180),
	)
	short_desc = Column(
		String(400),
	)
	file_type = Column(
		String(10)
	)
	file = Column(
		String(180),
	)
	account_id = Column(
		Integer, 
		ForeignKey('accounts.id')
	)
	account = relationship(
		'Account', 
		back_populates='articles'
	)