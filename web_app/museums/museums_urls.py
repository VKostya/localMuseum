from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pony.orm import db_session
from db.base import Museums, Subscriptions
from db.scripts.museums import select_with_id, validate_id
from db.scripts.posts import select_museum_posts
from db.scripts.subs import add_sub, del_sub, sub_exists
from db.scripts.users import get_subs_email
from schemas.museums import MuseumRead
from utils.auth import get_role, validate_user_role_not_null
from web_api.auth.router_auth import get_current_user_from_token

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, msg: str = None):
    token = request.cookies.get("access_token")
    user_role = 0
    if token:
        user_role = get_role(request=request)
    with db_session:
        museums = Museums.select()
        result = [MuseumRead.from_orm(m) for m in museums]
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {
            "request": request,
            "museums": result,
            "msg": msg,
            "user": user_role,
            "text": "Найти музей",
        },
    )


@router.get("/museum/{id}")
def museum_detail(id: int, request: Request):
    token = request.cookies.get("access_token")
    user_role = 0
    is_sub = False
    if token:
        user_role = get_role(request=request)
        user = get_current_user_from_token(token.split()[1])
        is_sub = sub_exists(museum_id=id, user_id=user.id)
    validate_id(id)
    mus = select_with_id(id=id)
    posts = select_museum_posts(id=id)
    posts = posts[::-1]
    return templates.TemplateResponse(
        "museums/details.html",
        {
            "request": request,
            "mus": mus,
            "user": user_role,
            "id": id,
            "is_sub": is_sub,
            "posts": posts,
        },
    )


@router.get("/favorite")
def fav_museums(request: Request):
    user_role = validate_user_role_not_null(request)
    token = request.cookies.get("access_token")
    user = get_current_user_from_token(token.split()[1])
    result = []
    with db_session:
        museums_id = Subscriptions.select(lambda s: s.user_id == user.id)
        for m in museums_id:
            museum = Museums.select(lambda s: s.id == m.museum_id)
            result.append([MuseumRead.from_orm(m) for m in museum])
        result = [m[0] for m in result]
        print(result[0].title)
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {
            "request": request,
            "museums": result,
            "user": user_role,
            "text": "Отслеживаемые музеи",
        },
    )


def is_subscriber(request, id):
    user_role = validate_user_role_not_null(request)
    validate_id(id)
    token = request.cookies.get("access_token")
    user = get_current_user_from_token(token.split()[1])
    is_sub = sub_exists(museum_id=id, user_id=user.id)
    return is_sub, user


@router.post("/sub/{id}")
def subscribe(id: int, request: Request):
    is_sub, user = is_subscriber(request=request, id=id)
    if is_sub:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Вы уже подписаны"
        )
    add_sub(museum_id=id, user_id=user.id)
    response = RedirectResponse(url=f"/museum/{id}", status_code=status.HTTP_302_FOUND)
    return response


@router.post("/unsub/{id}")
def subscribe(id: int, request: Request):
    is_sub, user = is_subscriber(request=request, id=id)
    if not is_sub:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Вы уже отписаны"
        )
    del_sub(museum_id=id, user_id=user.id)
    response = RedirectResponse(url=f"/museum/{id}", status_code=status.HTTP_302_FOUND)
    return response
