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
from app.vendors.utils.gate import gate
from app.http.api.auth import (
    get_current_user,
    Account as AccountAuth,
)
from . import services as srv
from . import schemas as sch
from app.config import cfg


adm_account = APIRouter(
    prefix = '/account',
    tags=['account'], 
)



@adm_account.post('/list/', 
    response_model=list[sch.AccountInItem], 
    status_code=status.HTTP_200_OK
)
async def read_accounts(skip: int = 0, limit: int = cfg.items_in_list, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_user)
):
    gate.allow(['allow_admin'], account)
    return srv.get_accounts(db, skip=skip, limit=limit)



@adm_account.get("/{account_id}/show/", 
    response_model=sch.AccountInItem,
    status_code=status.HTTP_200_OK
)
def read_account(account_id: int, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_user)
):
    gate.allow(['allow_admin'], account)
    return srv.get_account(db, account_id=account_id)



@adm_account.post('/create/', 
    response_model=sch.AccountInCreate,
    status_code=status.HTTP_201_CREATED
)
def create_account(account_data: sch.AccountInCreate, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_user)
):
    gate.allow(['allow_admin'], account)
    return srv.create_account(db, account_data=account_data)



@adm_account.put('/{account_id}/update/', 
    response_model=sch.AccountInUpdate,
    status_code=status.HTTP_202_ACCEPTED
)
def update_account(account_id: int, account_data: sch.AccountInUpdate, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_user)
):
    gate.allow(['allow_admin'], account)
    return srv.update_account(db, account_id=account_id, account_data=account_data)



@adm_account.delete('/{account_id}/delete/', 
    response_model=sch.AccountIn,
)
async def delete_account(account_id: int, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_user)
):
    gate.allow(['allow_admin'], account)
    srv.delete_account(db, account_id=account_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

