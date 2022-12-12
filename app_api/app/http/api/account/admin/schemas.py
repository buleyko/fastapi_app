from pydantic import (
	BaseModel, 
	ValidationError, 
	validator,
)
from app.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)


class AccountInItem(BaseModel):
	id: int
	first_name: str
	last_name: str
	email: str 
	username: str
	sex: bool
	articles_count: int | None = None

	class Config:
		orm_mode = True


class ProfileInBase(BaseModel):
	first_name: str
	last_name: str
	sex: bool = False

class ProfileIn(ProfileInBase):
	id: int 
	class Config:
		orm_mode = True

class ProfileInCreate(ProfileInBase):
	pass 

class ProfileInUpdate(ProfileInBase):
	pass 


class AccountInBase(BaseModel):
	email: str 
	username: str
	is_blocked: bool = False
	is_shown: bool = True

	@validator('email')
	def email_validation(cls, v):
		if not email_validation_check(v):
			raise ValueError('not valid email')
		return v

	@validator('username')
	def username_alphanumeric(cls, v):
		assert v.isalnum(), 'must be alphanumeric'
		return v

class AccountIn(AccountInBase):
	id: int 

	class Config:
		orm_mode = True

class AccountInCreate(AccountInBase):
	password: str
	password_confirmation: str

	profile: ProfileInCreate

	@validator('password')
	def password_validation(cls, v):
		if not passwd_validation_check(v):
			raise ValueError('not valid password')
		return v

	@validator('password_confirmation')
	def passwords_match(cls, v, values, **kwargs):
		if 'password' in values and v != values['password']:
			raise ValueError('passwords do not match')
		return v

class AccountInUpdate(AccountInBase):
	password: str
	password_confirmation: str

	profile: ProfileInUpdate

	@validator('password')
	def password_validation(cls, v):
		if not passwd_validation_check(v):
			raise ValueError('not valid password')
		return v

	@validator('password_confirmation')
	def passwords_match(cls, v, values, **kwargs):
		if 'password' in values and v != values['password']:
			raise ValueError('passwords do not match')
		return v
