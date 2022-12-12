from app.vendors.dependencies.database import DB
from app.http.api.auth.utils.jwt import create_token
from fastapi import (
	HTTPException,
	status,
)
from sqlalchemy import (
	or_, 
	insert,
)
from app import models as mdl
from . import schemas as sch
from app.config import cfg



def register_new_user(db: DB, account_data: sch.AccountCreate) -> sch.Token:
	account = db.session.execute(
		db.select(mdl.Account).filter(or_(
			mdl.Account.username == account_data.username, 
			mdl.Account.email == account_data.email
		))
	).scalar()
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
		sex=True if account_data.profile.sex == 'female' else False,
		account_id=account.id
	)
	db.session.add(profile)
	db.session.commit()

	return create_token(account)


def authenticate_user(db: DB, username: str, password: str) -> sch.Token:
	account = db.session.execute(
		db.select(mdl.Account).filter_by(username=username)
	).scalar()
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