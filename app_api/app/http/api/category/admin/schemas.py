from pydantic import (
	BaseModel, 
	ValidationError, 
	validator,
	Field,
)
from typing import Any
from enum import Enum
from app.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)


class CategoryInItem(BaseModel):
	id: int
	name: dict
	short_desc: dict
	is_blocked: bool
	is_shown: bool
	# child_count: int | None = None
	articles_count: int | None = None
	class Config:
		orm_mode = True


class ParentCategory(BaseModel):
	id: int
	name: dict
	short_desc: dict
	class Config:
		orm_mode = True

# class ChildCategory(BaseModel):
# 	id: int
# 	name: dict
# 	short_desc: dict
# 	class Config:
# 		orm_mode = True

class CategoryInBase(BaseModel):
	name: dict
	short_desc: dict
	is_blocked: bool
	is_shown: bool
	

class CategoryIn(CategoryInBase):
	id: int 
	parent: ParentCategory | None = None
	class Config:
		orm_mode = True

class CategoryInCreate(CategoryInBase):
	parent_id: int | None = None
	
class CategoryInUpdate(CategoryInBase):
	parent_id: int | None = None
	