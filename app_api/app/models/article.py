from app.vendors.base.database import Base
from sqlalchemy.orm import (
	relationship,
	backref,
)
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
)
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	Text,
	JSON,
)


class Article(ValidMixin, TimestampsMixin, Base):
	__tablename__ = 'articles'

	category_id = Column(
		Integer, 
		ForeignKey('categories.id')
	)
	category = relationship(
		'Category', 
		back_populates='articles'
	)
	data = relationship(
		'ArticleData', 
		back_populates='article',
	)
	comments = relationship(
		'Comment', 
		back_populates='article'
	)
	account_id = Column(
		Integer, 
		ForeignKey('accounts.id')
	)
	account = relationship(
		'Account', 
		back_populates='articles'
	)



class ArticleData(Base):
	__tablename__ = 'articles_datas'

	lang = Column(
		String(10), 
	) 
	name = Column(
		String,
	)
	short_desc = Column(
		String,
	)
	body = Column(
		Text, 
	)
	article_id = Column(
		Integer, 
		ForeignKey('articles.id'),
	)
	article = relationship(
		'Article', 
		back_populates='data',
	)


class Comment(TimestampsMixin, Base):
	__tablename__ = 'comments'

	username = Column(
		String(120),
		nullable=False,
	) 
	text = Column(
		Text, 
	)
	article_id = Column(
		Integer, 
		ForeignKey('articles.id'),
	)
	article = relationship(
		'Article', 
		back_populates='comments',
	)
	parent_id = Column(
		Integer, 
		ForeignKey('comments.id'),
		nullable=True,
	)
	children = relationship(
		'Comment', 
		backref=backref('parent', remote_side='Comment.id')
	)