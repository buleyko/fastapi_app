from pydantic import (
	BaseModel, 
	ValidationError, 
	validator,
	Field,
)


class ArticleInItem(BaseModel):
	id: int 
	name: str | None
	user: str
	category_name: dict
	langs: str | None
	comments_count: int | None = None
	class Config:
		orm_mode = True


class ArticleDataInBase(BaseModel):
	lang: str
	name: str
	short_desc: str
	body: str

class ArticleDataIn(ArticleDataInBase):
	id: int 
	class Config:
		orm_mode = True

class ArticleDataInCreate(ArticleDataInBase):
	pass 

class ArticleDataInUpdate(ArticleDataInBase):
	pass


class ArticleInBase(BaseModel):
	data: list[ArticleDataIn] = []


class CategoryIn(BaseModel):
	id: int 
	name: dict
	short_desc: dict
	class Config:
		orm_mode = True

class AccountIn(BaseModel):
	id: int 
	username: str
	class Config:
		orm_mode = True

class ArticleIn(ArticleInBase):
	id: int
	account: AccountIn
	category: CategoryIn
	is_blocked: bool = False
	is_shown: bool = True
	class Config:
		orm_mode = True

class ArticleInCreate(ArticleInBase):
	category_id: int
	account_id: int
	data: list[ArticleDataInCreate] = []

class ArticleInUpdate(ArticleInBase):
	category_id: int
	account_id: int
	data: list[ArticleDataInUpdate] = []

