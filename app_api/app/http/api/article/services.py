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
from sqlalchemy.orm import aliased
from app import models as mdl
from . import schemas as sch
from app.config import cfg



def get_articles(db: DB, skip: int = 0, limit: int = cfg.items_in_list, lang: str = cfg.default_lang):
	select_articles = db.select(
			mdl.Article.id, 
			mdl.Account.username.label('user'), 
			mdl.Category.name.label('category_name'),
			mdl.ArticleData.name.label('name'),
			func.count(mdl.Comment.id).label('comments_count')
		).\
		filter_by(is_blocked=False, is_shown=True).\
		outerjoin(mdl.Category).\
		outerjoin(mdl.Account).\
		outerjoin(mdl.ArticleData).\
		filter(mdl.ArticleData.lang==lang).\
		outerjoin(mdl.Article.comments).\
		group_by(mdl.Article.id).\
		offset(skip).limit(limit).\
		order_by(desc(mdl.Article.created_at))
	articles = db.session.execute(select_articles).all()
	return articles



def get_article(db: DB, article_id: int):
	select_article = db.select(mdl.Article).filter_by(id=article_id).\
		filter_by(is_blocked=False, is_shown=True)
	article = db.session.execute(select_article).scalar()
	if article is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		)
	return article