from .auth.api import auth
from .account.api import account
from .account.admin.api import adm_account


routers = [
	auth,
	account,
]


adm_routers = [
	adm_account,
]