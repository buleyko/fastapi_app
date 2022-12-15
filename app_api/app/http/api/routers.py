from .auth.api import auth
from .account.api import account
from .account.admin.api import adm_account
from .category.api import category
from .category.admin.api import adm_category


routers = [
	auth,
	account,
	category,
]


adm_routers = [
	adm_account,
	adm_category,
]