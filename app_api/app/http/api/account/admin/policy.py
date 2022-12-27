from app.vendors.utils.gate import gate
from fastapi import Depends
from app.http.api.auth import (
    get_current_user,
    Account as AccountAuth,
)



async def get_current_account_for_show_list(account: AccountAuth = Depends(get_current_user)):
	gate.allow(['allow_admin', 'show_category_list'], account)
	return account

async def get_current_account_for_show_item(account: AccountAuth = Depends(get_current_user)):
	gate.allow(['allow_admin', 'show_category_item'], account)
	return account

async def get_current_account_for_create(account: AccountAuth = Depends(get_current_user)):
	gate.allow(['allow_admin', 'create_category'], account)
	return account

async def get_current_account_for_update(account: AccountAuth = Depends(get_current_user)):
	gate.allow(['allow_admin', 'update_category'], account)
	return account

async def get_current_account_for_delete(account: AccountAuth = Depends(get_current_user)):
	gate.allow(['allow_admin', 'delete_category'], account)
	return account