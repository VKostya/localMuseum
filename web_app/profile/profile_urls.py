from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from db.scripts.users import (
    select_user_email,
    update_email,
    update_notifications,
    update_pass,
    update_verif,
)
from db.scripts.verifications import (
    add_verification_pair,
    check_ver_attempt,
    correct_hash,
    remove_verif_pair,
    verif_pair,
)
from utils.auth import get_role, validate_user_role_not_null
from utils.mail import send_ver_mail
from utils.security import get_unique_hash
from web_api.auth.router_auth import get_current_user_from_token
from fastapi.responses import RedirectResponse

from web_app.profile.profile_form import ChangePassForm, EmailForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def profile_page(request: Request):
    user_role = validate_user_role_not_null(request)
    token = request.cookies.get("access_token")
    user = get_current_user_from_token(token.split()[1])
    is_verified = user.is_valid
    send_notif = user.send_notifications
    return templates.TemplateResponse(
        "general_pages/profile.html",
        {
            "request": request,
            "user": user_role,
            "is_verified": is_verified,
            "send_notif": send_notif,
        },
    )


def change_notification_status(request: Request, value):
    user_role = validate_user_role_not_null(request)
    token = request.cookies.get("access_token")
    user = get_current_user_from_token(token.split()[1])
    update_notifications(user.id, value=value)
    response = RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
    return response


@router.post("/notify_on")
def turn_notif_on(request: Request):
    return change_notification_status(request=request, value=1)


@router.post("/notify_off")
def turn_notif_off(request: Request):
    return change_notification_status(request=request, value=0)


@router.get("/change_password")
def change_password(request: Request):
    user_role = validate_user_role_not_null(request)
    return templates.TemplateResponse(
        "auth/change_password.html",
        {
            "request": request,
            "user": user_role,
        },
    )


@router.get("/change_email")
def change_email(request: Request):
    user_role = validate_user_role_not_null(request)
    return templates.TemplateResponse(
        "auth/change_email.html",
        {
            "request": request,
            "user": user_role,
        },
    )


@router.post("/change_password")
async def change_password(request: Request):
    user_role = validate_user_role_not_null(request)
    token = request.cookies.get("access_token")
    form = ChangePassForm(request)
    await form.load_data()
    if await form.is_valid():
        user = get_current_user_from_token(token.split()[1])
        update_pass(id=user.id, value=form.password)
        response = RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
        return response
    return templates.TemplateResponse("auth/change_password.html", form.__dict__)


@router.post("/change_email")
async def change_email(request: Request):
    user_role = validate_user_role_not_null(request)
    token = request.cookies.get("access_token")
    form = EmailForm(request)
    await form.load_data()
    if await form.is_valid():
        if select_user_email(form.email):
            form.__dict__.get("errors").append(
                "Пользователь с таким адресом почты уже существует"
            )
            return templates.TemplateResponse("auth/change_email.html", form.__dict__)

        user = get_current_user_from_token(token.split()[1])
        update_email(id=user.id, value=form.email)

        response = RedirectResponse(url="/logout", status_code=status.HTTP_302_FOUND)
        return response
    return templates.TemplateResponse("auth/change_email.html", form.__dict__)


@router.get("/verify")
async def verify_email(request: Request, background_tasks: BackgroundTasks):
    user_role = validate_user_role_not_null(request)
    token = request.cookies.get("access_token")
    user = get_current_user_from_token(token.split()[1])
    if check_ver_attempt(user.id):
        hash_token = get_unique_hash()
        add_verification_pair(user_id=user.id, hash_code=hash_token)
        background_tasks.add_task(
            send_ver_mail, user.id, url=request.url._url, message=hash_token
        )
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="UNPROCESSABLE_ENTITY"
    )


@router.get("/verify/{id}")
async def verify_token(request: Request, id: str):
    if correct_hash(id):
        token = request.cookies.get("access_token")
        user = get_current_user_from_token(token.split()[1])
        if verif_pair(user_id=user.id, hash_code=id):
            update_verif(user.id)
            remove_verif_pair(user.id)
            response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
            return response
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
