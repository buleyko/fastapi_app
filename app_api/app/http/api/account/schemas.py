from pydantic import BaseModel



class AccountOutBase(BaseModel):
	first_name: str
	last_name: str
	email: str 
	username: str
	sex: bool
	articles_count: int | None = None

	
class AccountOutItem(AccountOutBase):
	id: int 

	class Config:
		orm_mode = True
