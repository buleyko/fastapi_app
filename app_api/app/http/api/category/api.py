from app.vendors.base.router import AppRoute
from fastapi import (
    Depends, 
    APIRouter, 
    Response, 
    HTTPException,
    status, 
)
from app.vendors.dependencies.database import (
    get_db, 
    DB,
)
from . import services as srv
from . import schemas as sch
from app.config import cfg


category = APIRouter(
    route_class=AppRoute, 
    prefix = '/category',
    tags = ['category'], 
)



@category.post('/list/', 
    response_model=list[sch.CategoryOutItem],
    status_code=status.HTTP_200_OK
)
async def read_categories(skip: int = 0, limit: int = cfg.items_in_list, db: DB = Depends(get_db)):
    return srv.get_categories(db, skip=skip, limit=limit)


@category.get('/{category_id}/show/', 
    response_model=sch.CategoryOut,
    status_code=status.HTTP_200_OK
)
async def read_category(category_id: int, db: DB = Depends(get_db)):
    return srv.get_category(db, category_id=category_id)


@category.get('/{category_id}/articles/', 
    response_model=list[sch.ArticleOut],
    status_code=status.HTTP_200_OK
)
async def read_category_articles(category_id: int, skip: int = 0, limit: int = cfg.items_in_list, 
    lang: str = cfg.default_lang, db: DB = Depends(get_db)
):
    return srv.get_category_articles(db, category_id=category_id, skip=skip, limit=limit, lang=lang)
