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



def get_categories(db: DB, skip: int = 0, limit: int = cfg.items_in_list):
	select_categories = db.select(
			mdl.Category.id, mdl.Category.name, mdl.Category.short_desc,
			func.count(mdl.Article.id).label('articles_count'),
		).\
		filter_by(is_blocked=False, is_shown=True).\
		outerjoin(mdl.Category.articles).\
		group_by(mdl.Category.name).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	categories = db.session.execute(select_categories).all()
	return categories


def get_category(db: DB, category_id: int):
	select_category = db.select(mdl.Category).filter_by(id=category_id).\
		filter_by(is_blocked=False, is_shown=True)
	category = db.session.execute(select_category).scalar()
	if category is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		)
	return category


def get_category_articles(db: DB, category_id: int, skip: int = 0, limit: int = cfg.items_in_list, lang: str = cfg.default_lang):
	select_articles = db.select(
			mdl.Article.id, mdl.ArticleData.name, mdl.ArticleData.short_desc,
		).\
		filter_by(category_id=category_id).\
		filter_by(is_blocked=False, is_shown=True).\
		outerjoin(mdl.Article.data).\
		filter_by(lang='en').\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	articles = db.session.execute(select_articles).all()
	return articles


