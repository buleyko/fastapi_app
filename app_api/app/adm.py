from app.vendors.base.app import AppFastApi
from app.http.middlewares import adm_middlewares
from app.http.api.routers import adm_routers
from app.factories import (
	middlewares_factory, 
	routers_factory,
)

__all__ = ('create_adm_app',)


def create_adm_app():
	adm_app = AppFastApi()
	middlewares_factory(adm_app, adm_middlewares)
	routers_factory(adm_app, adm_routers)
	return adm_app