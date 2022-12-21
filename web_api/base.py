from fastapi import APIRouter
from web_api.museums import router_museums

api_router = APIRouter()
api_router.include_router(router_museums.router, prefix="/museum")
