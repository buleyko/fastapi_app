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
from app.vendors.utils.gate import gate
from app.http.api.auth import (
    get_current_user,
    Account as AccountAuth,
)
from . import services as srv
from . import schemas as sch
from app.config import cfg


adm_article = APIRouter(
    prefix = '/article',
    tags=['article'], 
)


async def get_current_account_by_gate(account: AccountAuth = Depends(get_current_user)):
    gate.allow(['allow_admin'], account)
    return account


@adm_article.post('/list/', 
    response_model=list[sch.ArticleInItem], 
    status_code=status.HTTP_200_OK
)
async def read_articles(skip: int = 0, limit: int = cfg.items_in_list, 
    lang: str = cfg.default_lang, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.get_articles(db, skip=skip, limit=limit, lang=lang)



@adm_article.get('/{article_id}/show/', 
    response_model=sch.ArticleIn,
    status_code=status.HTTP_200_OK
)
def read_article(article_id: int, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.get_article(db, article_id=article_id)



@adm_article.post('/create/', 
    response_model=sch.ArticleIn,
    status_code=status.HTTP_201_CREATED
)
async def create_article(article_data: sch.ArticleInCreate, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.create_article(db, article_data=article_data)




@adm_article.put('/{article_id}/update/', 
    response_model=sch.ArticleIn,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_article(article_id: int, article_data: sch.ArticleInUpdate, db: DB = Depends(get_db), 
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    return srv.update_article(db, article_id=article_id, article_data=article_data)



@adm_article.delete('/{article_id}/delete/', 
    response_model=sch.ArticleIn,
)
async def delete_article(article_id: int, db: DB = Depends(get_db),
    account: AccountAuth = Depends(get_current_account_by_gate)
):
    srv.delete_article(db, article_id=article_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

