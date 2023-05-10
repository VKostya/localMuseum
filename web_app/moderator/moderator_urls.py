from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Response, status
from fastapi.templating import Jinja2Templates
from db.base import Museums, Posts
from db.scripts.museums import select_with_id, validate_id
from db.scripts.posts import add_post, delete_message_with_id, select_museum_posts
from schemas.museums import MuseumRead
from schemas.posts import PostsRead
from utils.auth import get_role
from utils.mail import send_notif_mail
from web_api.auth.router_auth import get_current_user_from_token
from fastapi.responses import RedirectResponse
from pony.orm import db_session
from datetime import datetime
from web_app.moderator.moderator_form import CreatePost

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


def validate_moderator(request):

    user_role = get_role(request=request)
    if user_role != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_correct_museum(request, id):
    validate_moderator(request=request)
    validate_id(id)
    token = request.cookies.get("access_token")
    user = get_current_user_from_token(token.split()[1])
    museums = select_with_id(id)
    if museums.manager_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/museums")
async def display_museums(request: Request):
    validate_moderator(request=request)
    token = request.cookies.get("access_token")
    user = get_current_user_from_token(token.split()[1])
    with db_session:
        museums = Museums.select(lambda m: m.manager_id == user.id)
        result = [MuseumRead.from_orm(m) for m in museums]
    return templates.TemplateResponse(
        "moderator/museum_list.html", {"request": request, "museums": result, "user": 2}
    )


@router.get("/museums/addMessage/{id}")
async def publish_message(id: int, request: Request):
    validate_correct_museum(request=request, id=id)
    museum = select_with_id(id)
    return templates.TemplateResponse(
        "moderator/message_form.html",
        {"request": request, "user": 2, "museum_name": museum.title},
    )


@router.post("/museums/addMessage/{id}")
async def publish_post(id: int, request: Request, background_tasks: BackgroundTasks):
    validate_correct_museum(request=request, id=id)
    form = CreatePost(request)
    await form.load_data()
    print(form.description)
    if form.is_valid():
        try:
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            add_post(text=form.description, date=dt_string, id=id)
            response = RedirectResponse(
                url="/moderate/museums", status_code=status.HTTP_302_FOUND
            )
            background_tasks.add_task(send_notif_mail, id, form.description)
            return response
        except Exception as e:
            form.__dict__.get("errors").append("Неверный формат данных")
            return templates.TemplateResponse(
                "moderator/message_form.html", form.__dict__
            )
    return templates.TemplateResponse("moderator/message_form.html", form.__dict__)


@router.get("/museums/deleteMessage/{id}")
async def display_messages(id: int, request: Request):
    validate_correct_museum(request=request, id=id)
    result = select_museum_posts(id=id)
    return templates.TemplateResponse(
        "moderator/delete_message.html",
        {"request": request, "posts": result, "user": 2, "museum_id": id},
    )


@router.get("/museums/delete/{museum_id}/{id}")
async def delete_message(id: int, request: Request, museum_id: int):
    validate_correct_museum(request=request, id=museum_id)
    delete_message_with_id(id)
    response = RedirectResponse(
        url=f"/moderate/museums/deleteMessage/{museum_id}",
        status_code=status.HTTP_302_FOUND,
    )
    return response
