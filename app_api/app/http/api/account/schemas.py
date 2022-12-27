from pydantic import (
	BaseModel, 
	Field,
	EmailStr
)
from enum import Enum
from typing import Any

class Photo(BaseModel):
	url: str | None = None # HttpUrl
	name: str | None = None

class AccountOutBase(BaseModel):
	first_name: str = Field(..., 
		title='First name',
        description='User first name',
       	min_length=3, max_length=30
    )
	last_name: str
	email: EmailStr | None
	username: str
	female: bool
	articles_count: int | None = None

	photo: Photo | None = None


class AccountOutItem(AccountOutBase):
	id: int = Field(..., gt=0)

	class Config:
		orm_mode = True


class AccountCreate(AccountOutBase):
	pass 