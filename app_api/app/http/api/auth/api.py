from fastapi.security import OAuth2PasswordRequestForm
from app.vendors.utils.gate import gate
from app.tasks.logger import write_to_log
from fastapi import (
    Depends, 
    APIRouter, 
    Response, 
    Request,
    HTTPException,
    status, 
    BackgroundTasks,
)
from app.vendors.dependencies.database import (
    get_db, 
    DB,
)
from .utils.jwt import get_current_user
from . import services as srv
from . import schemas as sch
from app.config import cfg


auth = APIRouter(
    prefix = '/auth',
    tags=['auth'], 
)



@auth.post('/sign-in/', 
    response_model=sch.Token, 
    status_code=status.HTTP_200_OK
)
async def auth_signin(
    background_tasks: BackgroundTasks,
    auth_data: OAuth2PasswordRequestForm = Depends(), 
    db: DB = Depends(get_db),
):
    user_token = srv.authenticate_user(db, auth_data.username, auth_data.password)
    srv.logger(background_tasks, auth_data.username, message='SIGN-IN')
    return user_token


@auth.post('/sign-up/', 
    response_model=sch.Token, 
    status_code=status.HTTP_201_CREATED
)
async def auth_signup(
    account_data: sch.AccountCreate, 
    request: Request,
    db: DB = Depends(get_db)
):
    return srv.register_new_user(request, db, account_data)



@auth.get('/activate-account/{uid}/{token}', 
    status_code=status.HTTP_202_ACCEPTED
)
async def activate_account(uid: str, token: str, db: DB = Depends(get_db)):
    return srv.activate_account(db, uid, token)