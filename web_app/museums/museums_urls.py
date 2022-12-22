from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pony.orm import db_session
from db.base import Museums
from db.scripts.museums import select_with_id, validate_id
from schemas.museums import MuseumRead
from web_api.auth.router_auth import get_current_role

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, msg: str = None):
    user_role = 0
    token = request.cookies.get("access_token")
    print(token)
    if token:
        user_role = get_current_role(token.split()[1])
    with db_session:
        museums = Museums.select()
        result = [MuseumRead.from_orm(m) for m in museums]
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {"request": request, "museums": result, "msg": msg, "user": user_role},
    )


@router.get("/museum/{id}")
def job_detail(id: int, request: Request):
    user_role = 0
    token = request.cookies.get("access_token")
    if token:
        user_role = get_current_role(token.split()[1])
    validate_id(id)
    mus = select_with_id(id=id)
    return templates.TemplateResponse(
        "museums/details.html", {"request": request, "mus": mus, "user": user_role}
    )
