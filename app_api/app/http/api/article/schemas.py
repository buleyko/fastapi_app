from pydantic import BaseModel, Field
from enum import Enum
from typing import Any



class CategoryOut(BaseModel):
	id: int 
	name: dict
	short_desc: dict
	class Config:
		orm_mode = True

class ArticleData(BaseModel):
	lang: str
	name: str
	short_desc: str
	body: str
	class Config:
		orm_mode = True

class AccountOut(BaseModel):
	id: int 
	username: str
	class Config:
		orm_mode = True

class ArticleOutBase(BaseModel):
	name: str | None
	user: str
	category_name: dict
	comments_count: int | None = None


class ArticleOutItem(ArticleOutBase):
	id: int 
	class Config:
		orm_mode = True


class ArticleOut(BaseModel):
	id: int
	account: AccountOut
	category: CategoryOut
	data: list[ArticleData] = []
	class Config:
		orm_mode = True

