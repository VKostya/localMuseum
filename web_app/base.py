from fastapi import APIRouter
from web_app.museums import museums_urls
from web_app.auth import login_urls
from web_app.admin import admin_urls
from web_app.profile import profile_urls
from web_app.moderator import moderator_urls

app_router = APIRouter()
app_router.include_router(museums_urls.router)
app_router.include_router(login_urls.router)
app_router.include_router(admin_urls.router, prefix="/admin")
app_router.include_router(profile_urls.router, prefix="/profile")
app_router.include_router(moderator_urls.router, prefix="/moderate")
