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
from sqlalchemy.orm import aliased
from app import models as mdl
from . import schemas as sch
from app.config import cfg




def get_articles(db: DB, skip: int = 0, limit: int = cfg.items_in_list, lang: str = cfg.default_lang):
	D = aliased(mdl.ArticleData)
	select_articles = db.select(
			mdl.Article.id, 
			mdl.Account.username.label('user'), 
			mdl.Category.name.label('category_name'),
			mdl.ArticleData.name.label('name'),
			func.group_concat(D.lang.distinct()).label('langs'),
			func.count(mdl.Comment.id).label('comments_count')
		).\
		outerjoin(mdl.Category).\
		outerjoin(mdl.Account).\
		outerjoin(mdl.ArticleData, 
			mdl.ArticleData.article_id==mdl.Article.id, 
			mdl.ArticleData.lang==lang
		).\
		outerjoin(D, D.article_id==mdl.Article.id).\
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


def create_article(db: DB, article_data: sch.ArticleInCreate):
	new_article = mdl.Article(
		category_id = article_data.category_id,
		account_id = article_data.account_id,
	)
	db.session.add(new_article)
	db.session.commit()
	db.session.refresh(new_article)

	for data in article_data.data:
		new_data = mdl.ArticleData(
			lang = data.lang,
			name = data.name,
			short_desc = data.short_desc,
			body = data.body,
			article_id = new_article.id,
		)
		db.session.add(new_data)
	db.session.commit()
	return new_article



def update_article(db: DB, article_id: int, article_data: sch.ArticleInUpdate):
	article = mdl.Article.get_first_item_by_filter(db, id=article_id)
	if article is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Article not found'
		) from None

	article.category_id = article_data.category_id,
	article.account_id = article_data.account_id,
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)

	for data in article_data.data:
		art_data = mdl.ArticleData.get_first_item_by_filter(db, id=article.id, lang=data.lang)
		if art_data is not None:
			art_data.name = data.name
			art_data.short_desc = data.short_desc
			art_data.body = data.body
			db.session.add(art_data)
	db.session.commit()
	return article



def delete_article(db: DB, article_id: int):
	article = mdl.Article.get_first_item_by_filter(db, id=article_id)
	if not article:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		) from None
	select_data = db.select(mdl.ArticleData).filter_by(id=article.id)
	article_data = db.session.execute(select_data).scalar()
	for data in article_data:
		db.session.delete(data)
	db.session.delete(article)
	db.session.commit()


