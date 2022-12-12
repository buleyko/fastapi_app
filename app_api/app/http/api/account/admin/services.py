from app.vendors.dependencies.database import DB
from sqlalchemy.orm.exc import NoResultFound
from fastapi import (
	HTTPException,
	status,
)
from sqlalchemy import (
	func, 
	desc,
)
from app import models as mdl
from . import schemas as sch
from app.config import cfg


def get_item_by_id(db: DB, model, id):
	item = db.session.execute(
		db.select(model).filter_by(id=id)
	).scalar()
	if not item:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		)
	return item

def check_account_uniqueness_by(db: DB, email: str, username: str):
	account = db.session.execute(
		db.select(mdl.Account).filter(or_(
			mdl.Account.username == username, 
			mdl.Account.email == email
		))
	).scalar()
	if account is not None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Username or email not unique',
		)


def get_accounts(db: DB, skip: int = 0, limit: int = cfg.items_in_list):
	select_accounts = db.select(
			mdl.Account.id, mdl.Account.email, mdl.Account.username,
			mdl.Profile.first_name, mdl.Profile.last_name, mdl.Profile.sex,
			func.count(mdl.Article.id).label('articles_count')
		).\
		outerjoin(mdl.Account.articles).outerjoin(mdl.Account.profile).\
		group_by(mdl.Account.username).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	accounts = db.session.execute(select_accounts).all()

	return accounts


def get_account(db: DB, account_id: int):
	select_account = db.select(
			mdl.Account.id, mdl.Account.email, mdl.Account.username,
			mdl.Profile.first_name, mdl.Profile.last_name, mdl.Profile.sex,
			func.count(mdl.Article.id).label('articles_count')
		).\
		filter_by(id=account_id).\
		outerjoin(mdl.Account.articles).outerjoin(mdl.Account.profile)
	try:
		account = db.session.execute(select_account).one()
	except NoResultFound:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		)
	return account


def create_account(db: DB, account_data: sch.AccountInCreate):
	check_account_uniqueness_by(db, account_data.email, account_data.username)

	new_account = mdl.Account(
		email=account_data.email,
		username=account_data.username,
		password=mdl.Account.get_hashed_password(account_data.password),
	)
	db.session.add(new_account)
	db.session.commit()
	db.session.refresh(new_account)

	new_profile = mdl.Profile(
		first_name=account_data.profile.first_name,
		last_name=account_data.profile.first_name,
		sex=True if account_data.profile.sex == 'female' else False,
		account_id=new_account.id
	)
	db.session.add(new_profile)
	db.session.commit()
	return new_account


def update_account(db: DB, account_id: int, account_data: sch.AccountInCreate):
	account = get_item_by_id(db, mdl.Account, account_id)
	
	account.email=account_data.email,
	account.username=account_data.username,
	account.password=mdl.Account.get_hashed_password(account_data.password),
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)

	profile = db.session.execute(
		db.select(mdl.Profile).filter_by(account_id=account.id)
	).scalar()
	if profile:
		profile.first_name=account_data.profile.first_name,
		profile.last_name=account_data.profile.first_name,
		profile.sex=True if account_data.profile.sex == 'female' else False,
		db.session.add(profile)
		db.session.commit()
	
	return account


def delete_account(db: DB, account_id: int):
	account = get_item_by_id(db, mdl.Account, account_id)
	db.session.delete(account)
	profile = db.session.execute(
		db.select(mdl.Profile).filter_by(account_id=account.id)
	).scalar()
	if profile:
		db.session.delete(profile)
	db.session.commit()