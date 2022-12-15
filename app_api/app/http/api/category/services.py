from app.vendors.dependencies.database import DB
from sqlalchemy.orm.exc import NoResultFound
from fastapi import (
	HTTPException,
	status,
)
from sqlalchemy import (
	func, 
	desc,
	case,
	literal_column,
)
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import coalesce
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

	# P = aliased(mdl.Category)
	# C = aliased(mdl.Category)
	# A = aliased(mdl.Article)
	# # func.count(C.id).label('child_count'),
	# # func.coalesce(Child.naughty, 0)
	# # func.count(case([(C.id)], else_=literal_column('NULL'))).label('child_count'),
	# select_categories2 = db.select(
	# 		P.id, P.name, P.short_desc,
	# 		func.count(C.id).label('child_count'),
	# 		func.count(A.account_id).label('articles_count'),
	# 	).\
	# 	filter_by(is_blocked=False, is_shown=True).\
	# 	outerjoin(C, C.parent_id==P.id).\
	# 	outerjoin(A, A.category_id==P.id).\
	# 	group_by(P.id).\
	# 	offset(skip).limit(limit).\
	# 	order_by(desc(P.created_at)).\
	# 	distinct()
	# categories2 = db.session.execute(select_categories2).all()
	# for q in categories2:
	# 	print(q)

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
		filter_by(lang=lang).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	articles = db.session.execute(select_articles).all()
	return articles


