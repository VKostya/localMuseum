from fastapi import APIRouter
from web_app.museums import museums_urls
from web_app.auth import login_urls

app_router = APIRouter()
app_router.include_router(museums_urls.router)
app_router.include_router(login_urls.router)
