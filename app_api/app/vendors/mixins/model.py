from sqlalchemy.orm import declarative_mixin
from sqlalchemy import func
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


