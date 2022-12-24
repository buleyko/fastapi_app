from sqlalchemy.orm import declarative_mixin
from app.vendors.helpers.image import resize_image
from datetime import timezone
from pathlib import Path
from sqlalchemy import (
    func, 
    or_,
)
from sqlalchemy import (
	Column, 
	DateTime,
    Boolean,
)
import aiofiles
from app.config import cfg



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
    # updated_at = Column(
    #     DateTime(timezone=True), 
    #     server_default=func.now(), 
    #     onupdate=func.now()
    # )


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


class ImageMixin:
    @staticmethod
    async def save_image(image_file, 
            thumb_size = cfg.photo_width, 
            file_allowed_exts = cfg.allowed_image_extensions, 
            ext_path = '',
            file_name = ''
        ):
        ''' Resize image to thumbnail width, 
            image_file: form.<image_name>.data or request.files[<image_name>] ''' 
        if image_file.filename == '':
            return None
        file_ext = image_file.filename.split('.')[-1]
        if file_ext not in file_allowed_exts:
            return None

        fp = cfg.root_path / cfg.upload_path_folder / image_file.filename
        async with aiofiles.open(fp, 'wb') as fh:
            while True:
                chunk = await image_file.read(cfg.chunk_size)
                if not chunk:
                    break
                await fh.write(chunk)

