from fastapi import APIRouter
from web_api.museums import router_museums
from web_api.admin import router_admin
from web_api.auth import router_auth

api_router = APIRouter()
api_router.include_router(router_museums.router, prefix="/museum")
api_router.include_router(router_admin.router, prefix="/admin")
api_router.include_router(router_auth.router, prefix="/auth")
