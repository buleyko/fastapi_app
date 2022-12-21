from fastapi.security import OAuth2PasswordRequestForm
from app.vendors.utils.gate import gate
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
from .utils.jwt import get_current_user
from . import services as srv
from . import schemas as sch


auth = APIRouter(
    prefix = '/auth',
    tags=['auth'], 
)



@auth.post('/sign-in/', 
    response_model=sch.Token, 
    status_code=status. HTTP_200_OK
)
async def auth_signin(
    auth_data: OAuth2PasswordRequestForm = Depends(), 
    db: DB = Depends(get_db)
):
    return srv.authenticate_user(db, auth_data.username, auth_data.password)


@auth.post('/sign-up/', 
    response_model=sch.Token, 
    status_code=status.HTTP_201_CREATED
)
async def auth_signup(
    account_data: sch.AccountCreate , 
    db: DB = Depends(get_db)
):
    return srv.register_new_user(db, account_data)


from app.services.celery.tasks import send_email

@auth.get('/mail-sender/')
async def mail_sender():
    try:
        # send_email.delay('qwertty')
        send_email.apply_async(
            args=['qwerty'], 
            countdown=60
        )
    except:
        return {'e': 'E'}
    return {'q': 'Q'}