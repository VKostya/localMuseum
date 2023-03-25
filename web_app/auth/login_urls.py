from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.templating import Jinja2Templates
from db.scripts.users import create_new_user, select_user_email
from web_api.auth.router_auth import login_for_access_token
from web_app.auth.login_form import LoginForm, RegisterForm
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    token = request.cookies.get("access_token")
    if token:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
async def login(request: Request):
    token = request.cookies.get("access_token")
    if token:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)


@router.get("/logout")
async def logout(request: Request, response: Response):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response


@router.get("/register")
def register(request: Request):
    token = request.cookies.get("access_token")
    if token:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
async def register(request: Request, response: Response):
    token = request.cookies.get("access_token")
    if token:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    form = RegisterForm(request)
    await form.load_data()
    if await form.is_valid():

        # check if user with this email exists
        if select_user_email(form.username):
            form.__dict__.get("errors").append(
                "Пользователь с таким адресом почты уже существует"
            )
            return templates.TemplateResponse("auth/register.html", form.__dict__)

        create_new_user(form.username, form.password)
        msg = "Вы зарегистрировались :)"
        form.__dict__.update(msg=msg)
        response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        return response
    return templates.TemplateResponse("auth/register.html", form.__dict__)
