from app.vendors.dependencies.database import DB
from sqlalchemy.orm.exc import NoResultFound
from app.vendors.helpers.file import write_file, aio_write_file
from fastapi import (
	HTTPException,
	status,
	UploadFile
)
from fastapi import UploadFile
from sqlalchemy import (
	func, 
	desc,
)
from app import models as mdl
from . import schemas as sch
from app.config import cfg


def get_accounts(db: DB, skip: int = 0, limit: int = cfg.items_in_list):
	select_accounts = db.select(
			mdl.Account.id, mdl.Account.email, mdl.Account.username,
			mdl.Profile.first_name, mdl.Profile.last_name, 
			mdl.Profile.female, mdl.Profile.photo,
			func.count(mdl.Article.id).label('articles_count')
		).\
		filter_by(is_blocked=False, is_shown=True, is_activated=True).\
		outerjoin(mdl.Account.articles).outerjoin(mdl.Account.profile).\
		group_by(mdl.Account.username).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	accounts = db.session.execute(select_accounts).all()

	return accounts


def get_account(db: DB, account_id: int):
	select_account = db.select(
			mdl.Account.id, mdl.Account.email, mdl.Account.username,
			mdl.Profile.first_name, mdl.Profile.last_name, 
			mdl.Profile.female, mdl.Profile.photo,
			func.count(mdl.Article.id).label('articles_count')
		).\
		filter_by(is_blocked=False, is_shown=True, is_activated=True).\
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



def video_upload(file):
	dir_path = cfg.root_path / cfg.upload_folder_dir / 'video'
	return write_file(file, dir_path)


# ---------------------------------------
# import shutil 
# import aiofiles
# async def images_upload(files):
# 	for file in files:
# 		file_path = cfg.root_path / cfg.upload_folder_dir / 'images' / file.filename
# 		with open(file_path, 'wb') as _fb:
# 			shutil.copyfileobj(file.file, _fb)
# 		return file.filename
# 		# async with aiofiles.open(file_path, 'wb') as fh:
# 		# 	while True:
# 		# 		chunk = await file.read(cfg.chunk_size)
# 		# 		if not chunk:
# 		# 			break
# 		# 		await fh.write(chunk)
