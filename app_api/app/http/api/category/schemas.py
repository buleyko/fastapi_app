from pydantic import BaseModel




class CategoryOutBase(BaseModel):
	name: dict
	short_desc: dict
	articles_count: int | None = None

class CategoryOutItem(CategoryOutBase):
	id: int 
	class Config:
		orm_mode = True



class ArticleBase(BaseModel):
	id: int

class Article(ArticleBase):
	class Config:
		orm_mode = True


class ParentCategory(BaseModel):
	id: int
	name: dict
	short_desc: dict
	class Config:
		orm_mode = True

class CategoryBase(BaseModel):
	name: dict
	short_desc: dict

class Category(CategoryBase):
	id: int
	parent: ParentCategory | None = None
	articles: list[Article] = []
	class Config:
		orm_mode = True


class ArticleOutBase(BaseModel):
	name: str | None = None
	short_desc: str | None = None

class ArticleOut(ArticleOutBase):
	id: int
	class Config:
		orm_mode = True