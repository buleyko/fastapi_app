from .auth.api import auth
from .account.api import account
from .account.admin.api import adm_account
from .category.api import category


routers = [
	auth,
	account,
	category,
]


adm_routers = [
	adm_account,
]