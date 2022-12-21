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




def get_categories(db: DB, skip: int = 0, limit: int = cfg.items_in_list):
	select_categories = db.select(
			mdl.Category.id, mdl.Category.name, mdl.Category.short_desc,
			mdl.Category.is_blocked, mdl.Category.is_shown,
			func.count(mdl.Article.id).label('articles_count'),
		).\
		outerjoin(mdl.Category.articles).\
		group_by(mdl.Category.id).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	categories = db.session.execute(select_categories).all()

	return categories



def get_category(db: DB, category_id: int):
	category = mdl.Category.get_first_item_by_filter(db, id=category_id)
	if category is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		) from None
	return category



def create_category(db: DB, category_data: sch.CategoryInCreate):
	parent_id = category_data.parent_id if category_data.parent_id else None
	new_category = mdl.Category(
		name = category_data.name,
		short_desc =  category_data.short_desc,
		is_blocked = category_data.is_blocked,
		is_shown = category_data.is_shown,
		parent_id = parent_id
	)
	db.session.add(new_category)
	db.session.commit()
	db.session.refresh(new_category)
	return new_category



def update_category(db: DB, category_id: int, category_data: sch.CategoryInUpdate):
	category = mdl.Category.get_first_item_by_filter(db, id=category_id)
	if category is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		) from None
	for field, value in category_data:
		setattr(category, field, value)
	db.session.add(category)
	db.session.commit()
	return category


def delete_category(db: DB, category_id: int):
	category = mdl.Category.get_first_item_by_filter(db, id=category_id)
	if category is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		) from None
	db.session.delete(category)
	db.session.commit()


'''
class ItemsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self, user_id: int) -> List[tables.Item]:
        items = (
            self.session
            .query(tables.Item)
            .filter(tables.Item.user_id == user_id)
            .order_by(
                tables.Item.date.desc(),
                tables.Item.id.desc(),
            )
            .all()
        )
        return items

    def get(
        self,
        user_id: int,
        Item_id: int
    ) -> tables.Item:
        Item = self._get(user_id, Item_id)
        return Item

    def create_many(
        self,
        user_id: int,
        Items_data: List[models.ItemCreate],
    ) -> List[tables.Item]:
        items = [
            tables.Item(
                **Item_data.dict(),
                user_id=user_id,
            )
            for Item_data in Items_data
        ]
        self.session.add_all(items)
        self.session.commit()
        return items

    def create(
        self,
        user_id: int,
        Item_data: models.ItemCreate,
    ) -> tables.Item:
        Item = tables.Item(
            **Item_data.dict(),
            user_id=user_id,
        )
        self.session.add(Item)
        self.session.commit()
        return Item

    def update(
        self,
        user_id: int,
        Item_id: int,
        Item_data: models.ItemUpdate,
    ) -> tables.Item:
        Item = self._get(user_id, Item_id)
        for field, value in Item_data:
            setattr(Item, field, value)
        self.session.commit()
        return Item

    def delete(
        self,
        user_id: int,
        Item_id: int,
    ):
        Item = self._get(user_id, Item_id)
        self.session.delete(Item)
        self.session.commit()

    def _get(self, user_id: int, Item_id: int) -> Optional[tables.Item]:
        Item = (
            self.session
            .query(tables.Item)
            .filter(
                tables.Item.user_id == user_id,
                tables.Item.id == Item_id,
            )
            .first()
        )
        if not Item:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return Item

'''


