from app.vendors.base.database import Base
from app.vendors.utils.crypto import password_context
from sqlalchemy.orm import (
	relationship,
	column_property,
	synonym,
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
	Boolean,
	JSON,
)


class Account(ValidMixin, TimestampsMixin, HelpersMixin, Base):
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



class Profile(HelpersMixin, Base):
	__tablename__ = 'profiles'

	first_name = Column(
		String(80)
	)
	last_name = Column(
		String(80)
	)
	photo = Column(
		String(255)
	)
	female = Column(
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

	full_name = column_property(first_name + ' ' + last_name)

	# gen = synonym('female')

	# @property
	# def sex(self):
	# 	return 'female' if self._sex else 'male'

	# @sex.setter
	# def sex(self, v):
	# 	self._sex = v == 'female'
