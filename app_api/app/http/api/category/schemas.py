from pydantic import BaseModel




class CategoryOutBase(BaseModel):
	name: dict
	short_desc: dict
	# child_count: int | None = None
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

class ChildCategory(BaseModel):
	id: int
	name: dict
	short_desc: dict
	class Config:
		orm_mode = True

class CategoryBase(BaseModel):
	name: dict
	short_desc: dict

class CategoryOut(CategoryBase):
	id: int
	parent: ParentCategory | None = None
	articles: list[Article] = []
	# children: list[ChildCategory] = []
	class Config:
		orm_mode = True


class ArticleOutBase(BaseModel):
	name: str | None = None
	short_desc: str | None = None

class ArticleOut(ArticleOutBase):
	id: int
	class Config:
		orm_mode = True