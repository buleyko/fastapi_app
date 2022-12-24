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


article = APIRouter(
    route_class=AppRoute, 
    prefix = '/article',
    tags=['article'], 
)



@article.get('/list/', 
    response_model=list[sch.ArticleOutItem], 
    status_code=status.HTTP_200_OK
)
async def read_articles(skip: int = 0, limit: int = cfg.items_in_list, db: DB = Depends(get_db)):
    return srv.get_articles(db, skip=skip, limit=limit)


@article.get('/{article_id}/show/', 
    response_model=sch.ArticleOut,
    status_code=status.HTTP_200_OK
)
def read_article(article_id: int, db: DB = Depends(get_db)):
    return srv.get_article(db, article_id=article_id)