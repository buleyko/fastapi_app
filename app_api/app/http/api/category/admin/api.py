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


adm_category = APIRouter(
    prefix = '/category',
    tags = ['category'], 
)


async def get_current_account_by_gate(account: AccountAuth = Depends(get_current_user)):
    gate.allow(['allow_admin'], account):
    return account


@adm_category.post('/list/', 
    response_model=list[sch.CategoryInItem], 
    status_code=status.HTTP_200_OK
)
async def read_categories(skip: int = 0, limit: int = cfg.items_in_list, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.get_categories(db, skip=skip, limit=limit)



@adm_category.get('/{category_id}/show/', 
    response_model=sch.CategoryIn,
    status_code=status.HTTP_200_OK
)
async def read_category(category_id: int, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.get_category(db, category_id=category_id)



@adm_category.post('/create/', 
    response_model=sch.CategoryIn,
    status_code=status.HTTP_201_CREATED
)
async def create_category(category_data: sch.CategoryInCreate, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.create_category(db, category_data=category_data)



@adm_category.put('/{category_id}/update/', 
    response_model=sch.CategoryIn,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_category(category_id: int, category_data: sch.CategoryInUpdate, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.update_category(db, category_id=category_id, category_data=category_data)



@adm_category.delete('/{category_id}/delete/', 
    response_model=sch.CategoryIn,
)
async def delete_category(category_id: int, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    srv.delete_category(db, category_id=category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

