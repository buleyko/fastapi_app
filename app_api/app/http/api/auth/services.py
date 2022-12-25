from app.vendors.dependencies.database import DB
from app.http.api.auth.utils.jwt import create_token
from app.services.celery.tasks import send_email
from app.vendors.helpers import mail as m
from app.tasks.logger import write_to_log
from fastapi import (
	Request,
	HTTPException,
	status,
)
import base64
from sqlalchemy import or_
from app import models as mdl
from . import schemas as sch
from app.config import cfg



def logger(background_tasks, username, message):
	background_tasks.add_task(write_to_log, username, message)
	

def register_new_user(request: Request, db: DB, account_data: sch.AccountCreate) -> sch.Token:
	account = mdl.Account.get_first_item_by_filter(
		db, _or=True, email=account_data.email, username=account_data.username
	)
	if account is not None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Username or email not unique',
			headers={'WWW-Authenticate': 'Bearer'},
		)

	account = mdl.Account(
		email=account_data.email,
		username=account_data.username,
		is_blocked=account_data.is_blocked,
		is_shown=account_data.is_shown,
		password=mdl.Account.get_hashed_password(account_data.password),
	)
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)

	profile = mdl.Profile(
		first_name=account_data.profile.first_name,
		last_name=account_data.profile.first_name,
		female=account_data.profile.female,
		account_id=account.id,
	)
	db.session.add(profile)
	db.session.commit()

	if cfg.activated_account_by_email:
		try:
			email_data = m.get_activate_account_mail(request, account, 'mail/activate_account.html')
			send_email.apply_async(
				args=[email_data], 
				countdown=60
			)
		except:
			pass 

	return create_token(account)


def authenticate_user(db: DB, username: str, password: str) -> sch.Token:
	account = mdl.Account.get_first_item_by_filter(db, username=username)
	if not account or not account.verify_password(password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Incorrect username or password',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	if not account.is_activated:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail='Not activated user',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	if account.is_blocked:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail='Blocked user',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	return create_token(account)


def activate_account(db: DB, uid: str, token: str):
	raw_uid = eval(base64.b64decode(uid))['uid']
	account_id = int(raw_uid.split(':')[0])
	account = mdl.Account.get_first_item_by_filter(db, id=account_id)
	account.is_activated = True
	db.session.add(account)
	db.session.commit()


