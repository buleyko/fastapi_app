from app.vendors.base.database import Base
from sqlalchemy.orm import relationship
from app.vendors.utils.crypto import password_context
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
)
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	Boolean,
	JSON,
)


class Account(ValidMixin, TimestampsMixin, Base):
	__tablename__ = 'accounts'

	email = Column(
		String, 
		unique=True
	)
	username = Column(
		String, 
		unique=True
	)
	password = Column(
		String
	)
	is_activated = Column(
		Boolean,
		default=False,
	)
	permissions = Column(
		JSON,
	)
	articles = relationship(
		'Article', 
		back_populates='account'
	)
	profile = relationship(
		'Profile', 
		back_populates='account',
		uselist=False
	)

	@staticmethod
	def get_hashed_password(password: str) -> str:
		return password_context.hash(password)

	def verify_password(self, password: str) -> bool:
		return password_context.verify(password, self.password)



class Profile(Base):
	__tablename__ = 'profiles'

	first_name = Column(
		String(80)
	)
	last_name = Column(
		String(80)
	)
	sex = Column(
		Boolean,
		default=True
	)
	account_id = Column(
		Integer, 
		ForeignKey('accounts.id')
	)
	account = relationship(
		'Account', 
		back_populates='profile'
	)
