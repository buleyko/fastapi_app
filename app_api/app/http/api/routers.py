from .auth.api import auth
from .account.api import account
from .account.admin.api import adm_account
from .category.api import category
from .category.admin.api import adm_category
from .article.api import article
from .article.admin.api import adm_article


routers = [
	auth,
	account,
	category,
	article,
]


adm_routers = [
	adm_account,
	adm_category,
	adm_article,
]