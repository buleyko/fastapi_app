from app.vendors.dependencies.database import DB
from sqlalchemy.orm.exc import NoResultFound
from fastapi import (
	HTTPException,
	status,
)
from sqlalchemy import (
	func, 
	desc,
	or_,
)
from app import models as mdl
from . import schemas as sch
from app.config import cfg



def get_accounts(db: DB, skip: int = 0, limit: int = cfg.items_in_list):
	select_accounts = db.select(
			mdl.Account.id, mdl.Account.email, mdl.Account.username,
			mdl.Account.is_blocked, mdl.Account.is_shown, mdl.Account.is_activated,
			mdl.Profile.first_name, mdl.Profile.last_name, 
			mdl.Profile.female, mdl.Profile.photo,
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
			mdl.Account.is_blocked, mdl.Account.is_shown, mdl.Account.is_activated,
			mdl.Profile.first_name, mdl.Profile.last_name, 
			mdl.Profile.female, mdl.Profile.photo,
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


def create_account_form(db: DB, bg_task, account_data: sch.AccountInCreate, photo):
	account = mdl.Account.get_first_item_by_filter(
		db, _or=True, email=account_data.email, username=account_data.username
	)
	if account is not None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Username or email not unique',
		) from None

	new_account = mdl.Account(
		email=account_data.email,
		username=account_data.username,
		is_blocked=account_data.is_blocked,
		is_shown=account_data.is_shown,
		password=mdl.Account.get_hashed_password(account_data.password),
	)
	db.session.add(new_account)
	db.session.commit()
	db.session.refresh(new_account)

	new_profile = mdl.Profile(
		first_name=account_data.profile.first_name,
		last_name=account_data.profile.first_name,
		female=account_data.profile.female,
		account_id=new_account.id,
	)
	if photo:
		ext_photo_path = f'images/account/{account_data.username}/profile'
		bg_task.add_task(mdl.Profile.save_and_resize_photo, photo, ext_photo_path, cfg.photo_width)
		# photo_file_subpath = mdl.Profile.save_and_resize_photo(photo, ext_photo_path, cfg.photo_width)
		# new_profile.photo=photo_file_subpath
		new_profile.photo=f'{ext_photo_path}/{photo.filename}'
	db.session.add(new_profile)
	db.session.commit()

	return new_account


def create_account(db: DB, account_data: sch.AccountInCreate):
	account = mdl.Account.get_first_item_by_filter(
		db, _or=True, email=account_data.email, username=account_data.username
	)
	if account is not None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Username or email not unique',
		) from None

	new_account = mdl.Account(
		email=account_data.email,
		username=account_data.username,
		is_blocked=account_data.is_blocked,
		is_shown=account_data.is_shown,
		password=mdl.Account.get_hashed_password(account_data.password),
	)
	db.session.add(new_account)
	db.session.commit()
	db.session.refresh(new_account)

	new_profile = mdl.Profile(
		first_name=account_data.profile.first_name,
		last_name=account_data.profile.first_name,
		female=account_data.profile.female,
		account_id=new_account.id,
	)
	db.session.add(new_profile)
	db.session.commit()
	return new_account


def update_account(db: DB, account_id: int, account_data: sch.AccountInUpdate):
	account = mdl.Account.get_first_item_by_filter(db, id=account_id)
	if account is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		) from None
	
	account.email=account_data.email
	account.username=account_data.username
	account.is_blocked=account_data.is_blocked
	account.is_shown=account_data.is_shown
	account.password=mdl.Account.get_hashed_password(account_data.password)
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)

	profile = mdl.Profile.get_first_item_by_filter(db, account_id=account.id)
	if profile is not None:
		profile.first_name=account_data.profile.first_name
		profile.last_name=account_data.profile.first_name
		female=account_data.profile.female
		db.session.add(profile)
		db.session.commit()
	
	return account


def delete_account(db: DB, account_id: int):
	account = mdl.Account.get_first_item_by_filter(db, id=account_id)
	if not account:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		) from None
	profile = mdl.Profile.get_first_item_by_filter(db, account_id=account.id)
	if profile is not None:
		db.session.delete(profile)
	# account.delete(synchronize_session=False)
	db.session.delete(account)
	db.session.commit()


