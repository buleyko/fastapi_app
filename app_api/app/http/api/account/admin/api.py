from fastapi import (
    Depends, 
    APIRouter, 
    Response, 
    HTTPException,
    status, 
    File, 
    UploadFile,
    Form,
)
from pydantic import EmailStr
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
from . import policy as pl 
from app.config import cfg


adm_account = APIRouter(
    prefix = '/account',
    tags=['account'], 
)

async def get_current_account_by_gate(account: AccountAuth = Depends(get_current_user)):
    gate.allow(['allow_admin'], account)
    return account


@adm_account.post('/list/', 
    response_model=list[sch.AccountInItem], 
    status_code=status.HTTP_200_OK
)
async def read_accounts(skip: int = 0, limit: int = cfg.items_in_list, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.get_accounts(db, skip=skip, limit=limit)



@adm_account.get('/{account_id}/show/', 
    response_model=sch.AccountInItem,
    status_code=status.HTTP_200_OK
)
async def read_account(account_id: int, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.get_account(db, account_id=account_id)



@adm_account.post('/create/', 
    response_model=sch.AccountIn,
    status_code=status.HTTP_201_CREATED
)
async def create_account(account_data: sch.AccountInCreate, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.create_account(db, account_data=account_data)



from app.vendors.helpers.file import async_write_file
from app.vendors.helpers.image import resize_image
@adm_account.post('/create-form/', 
    response_model=sch.AccountIn,
    status_code=status.HTTP_201_CREATED
)
async def create_account_form(
    first_name: str = Form(...),
    last_name: str = Form(...),
    female: bool = Form(...),
    email: EmailStr = Form(...),
    username: str = Form(...),
    is_blocked: bool = Form(...),
    is_shown: bool = Form(...),
    password: str = Form(...),
    password_confirmation: str = Form(...),
    photo: UploadFile | None = None,
    db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    profile_data = sch.ProfileInCreate(
        first_name = first_name,
        last_name = last_name,
        female = female,
        photo = None,
    )
    account_data = sch.AccountInCreate(
        email = email,
        username = username,
        is_blocked = is_blocked,
        is_shown = is_shown,
        password = password,
        password_confirmation = password_confirmation,
        profile = profile_data
    )
    return srv.create_account_form(db, account_data=account_data, photo=photo)




@adm_account.put('/{account_id}/update/', 
    response_model=sch.AccountIn,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_account(account_id: int, account_data: sch.AccountInUpdate, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.update_account(db, account_id=account_id, account_data=account_data)



@adm_account.delete('/{account_id}/delete/', 
    response_model=sch.AccountIn,
)
async def delete_account(account_id: int, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    srv.delete_account(db, account_id=account_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

