from pydantic import BaseModel, Field
from enum import Enum
from typing import Any

class AccountOutBase(BaseModel):
	first_name: str
	last_name: str
	email: str 
	username: str
	female: bool
	articles_count: int | None = None


class AccountOutItem(AccountOutBase):
	id: int 

	class Config:
		orm_mode = True

