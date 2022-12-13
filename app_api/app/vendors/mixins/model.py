from sqlalchemy.orm import declarative_mixin
from sqlalchemy import (
    func, 
    or_,
)
from sqlalchemy import (
	Column, 
	DateTime,
    Boolean,
)


@declarative_mixin
class TimestampsMixin:
    created_at = Column(
    	DateTime, 
    	default=func.now()
    )
    updated_at = Column(
    	DateTime, 
    	nullable=True,
    )


@declarative_mixin
class ValidMixin:
    is_blocked = Column(
        Boolean,
        default=True,
    )
    is_shown = Column(
        Boolean,
        default=False,
    )

class HelpersMixin:
    @classmethod
    def get_first_item_by_filter(cls, db, _or=False, **kwargs):
        if not _or:
            item_select = db.select(cls).filter_by(**kwargs)
        else:
            filters = [getattr(cls, k) == v for k, v in kwargs.items()]
            item_select = db.select(cls).filter(or_(False, *filters))
        item = db.session.execute(item_select).scalar()
        return item


