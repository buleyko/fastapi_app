from fastapi import (
    Depends, 
    APIRouter, 
    Response, 
    HTTPException,
    status, 
)
from app.vendors.dependencies.database import (
    get_db, 
    DB,
)
from . import services as srv
from . import schemas as sch
from app.config import cfg


account = APIRouter(
    prefix = '/account',
    tags=['account'], 
)



@account.post('/list/', 
    response_model=list[sch.AccountOutItem], 
    status_code=status. HTTP_200_OK
)
async def read_accounts(skip: int = 0, limit: int = cfg.items_in_list, db: DB = Depends(get_db)):
    return srv.get_accounts(db, skip=skip, limit=limit)


@account.get("/{account_id}/show/", 
    response_model=sch.AccountOutItem
)
def read_account(account_id: int, db: DB = Depends(get_db)):
    return srv.get_account(db, account_id=account_id)