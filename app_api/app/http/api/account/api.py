from app.vendors.base.router import AppRoute
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
    route_class=AppRoute, 
    prefix = '/account',
    tags=['account'], 
)



@account.get('/list/', 
    response_model=list[sch.AccountOutItem], 
    status_code=status.HTTP_200_OK
)
async def read_accounts(skip: int = 0, limit: int = cfg.items_in_list, db: DB = Depends(get_db)):
    return srv.get_accounts(db, skip=skip, limit=limit)


@account.get('/{account_id}/show/', 
    response_model=sch.AccountOutItem,
    status_code=status.HTTP_200_OK
)
async def read_account(account_id: int, db: DB = Depends(get_db)):
    return srv.get_account(db, account_id=account_id)


# ----------------------------------------------------
from fastapi import (
    File, 
    UploadFile,
)
# response_model=sch.AccountCreate,
# status_code=status.HTTP_200_OK
@account.post('/image-upload/')
async def read_account(files: list[UploadFile]):
    res = await srv.image_upload(files)
    return {'q': 'Q'}