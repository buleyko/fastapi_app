from pydantic import (
	BaseModel, 
	Field,
)
from enum import Enum
from typing import Any

class Photo(BaseModel):
	url: str | None = None # HttpUrl
	name: str | None = None

class AccountOutBase(BaseModel):
	first_name: str
	last_name: str
	email: str 
	username: str
	female: bool
	articles_count: int | None = None

	photo: Photo | None = None


class AccountOutItem(AccountOutBase):
	id: int 

	class Config:
		orm_mode = True



class AccountCreate(AccountOutBase):
	pass 