from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from db.base import Museums, Users
from db.scripts.museums import (
    delete_with_id,
    select_with_id,
    update_sql_data,
    upgate_image_url,
)
from db.scripts.users import select_user_with_id, update_role
from schemas.museums import MuseumRead
from pony.orm import db_session
from schemas.users import UserRead
from utils.auth import get_role
from utils.cloudinary_utils import load_to_cloudinary
from web_api.auth.router_auth import get_current_user_from_token
from web_app.admin.admin_form import MuseumCreateForm, UserRoleForm

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


def validate_admin(request):
    user_role = get_role(request=request)
    if user_role != 3:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/museums")
def list_museums(request: Request):
    validate_admin(request)
    with db_session:
        museums = Museums.select()
        result = [MuseumRead.from_orm(m) for m in museums]

    return templates.TemplateResponse(
        "admin/admin_museum.html", {"request": request, "museum": result, "user": 3}
    )


@router.get("/museums/deleteMuseum/{id}")
def list_museums(request: Request, id: int):
    validate_admin(request)
    delete_with_id(id)
    response = RedirectResponse(url="/admin/museums", status_code=status.HTTP_302_FOUND)
    return response


@router.get("/museum/addMuseum")
def add_museum(request: Request):
    validate_admin(request)
    return templates.TemplateResponse(
        "admin/add_form.html", {"request": request, "user": 3}
    )


@router.post("/museum/addMuseum")
async def add_museum(request: Request, file: UploadFile = File(...)):
    validate_admin(request)
    form = MuseumCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            form.__dict__.update(msg="Добавлено")
            response = templates.TemplateResponse("admin/add_form.html", form.__dict__)
            url = await load_to_cloudinary(form.title, file)
            with db_session:
                Museums(
                    title=form.title,
                    image_url=url,
                    description=form.description,
                    address=form.address,
                    contact_url=form.contact_url,
                    ticket_price=form.ticket_price,
                    schedule=form.schedule,
                    manager_id=form.manager_id,
                )
            return response
        except Exception as e:
            form.__dict__.get("errors").append("Неверный формат данных")
            return templates.TemplateResponse("admin/add_form.html", form.__dict__)
    return templates.TemplateResponse("admin/add_form.html", form.__dict__)


@router.get("/museums/changePicture/{id}")
async def reset_image(id: int, request: Request):
    validate_admin(request)
    museum = select_with_id(id)
    return templates.TemplateResponse(
        "admin/image_form.html", {"request": request, "user": 3, "mus": museum}
    )


@router.post("/museums/changePicture/{id}")
async def reset_image(id: int, request: Request, file: UploadFile = File(...)):
    validate_admin(request)
    museum = select_with_id(id)
    try:
        url = await load_to_cloudinary(museum.title, file)
    except:
        raise HTTPException(status_code=501, detail="Unable to load image")
    upgate_image_url(id, url)
    return templates.TemplateResponse(
        "admin/image_form.html",
        {"request": request, "user": 3, "msg": "Добавлено", "mus": museum},
    )


@router.get("/museums/changeInfo/{id}")
async def change_info(id: int, request: Request):
    validate_admin(request)
    museum = select_with_id(id)
    return templates.TemplateResponse(
        "admin/info_form.html", {"request": request, "user": 3, "mus": museum}
    )


@router.post("/museums/changeInfo/{id}")
async def change_info(id: int, request: Request):
    validate_admin(request)
    form = MuseumCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            update_sql_data(id=id, data=form)
            form.__dict__.update(msg="Изменено")
            response = RedirectResponse(
                url="/admin/museums", status_code=status.HTTP_302_FOUND
            )

            return response
        except Exception as e:
            form.__dict__.get("errors").append("Неверный формат данных")
            return templates.TemplateResponse("admin/info_form.html", form.__dict__)
    return templates.TemplateResponse("admin/info_form.html", form.__dict__)


@router.get("/users")
async def list_users(request: Request):
    validate_admin(request=request)
    token = request.cookies.get("access_token")
    user = get_current_user_from_token(token.split()[1])
    with db_session:
        users = Users.select(lambda u: u.id != user.id)
        result = [UserRead.from_orm(u) for u in users]
    return templates.TemplateResponse(
        "admin/admin_users.html", {"request": request, "users": result, "user": 3}
    )


@router.get("/users/changeRole/{id}")
async def reset_role(id: int, request: Request):
    validate_admin(request)
    user = select_user_with_id(id)
    return templates.TemplateResponse(
        "admin/change_role.html", {"request": request, "user": 3, "us": user}
    )


@router.post("/users/changeRole/{id}")
async def change_role(id: int, request: Request):
    validate_admin(request)
    form = UserRoleForm(request=request)
    user = select_user_with_id(id)
    await form.load_data()
    if form.is_valid():
        try:
            print(form.role)
            update_role(id, form.role)
            print(id)
            form.__dict__.update(msg="Изменено")
            response = RedirectResponse(
                url="/admin/users", status_code=status.HTTP_302_FOUND
            )
            return response
        except Exception as e:
            form.__dict__.get("errors").append("Неверный формат данных")
            return templates.TemplateResponse("admin/change_role.html", form.__dict__)
    return templates.TemplateResponse("admin/change_role.html", form.__dict__)
