from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("HTTP_errors/404.html", {"request": request})


async def not_authenticated_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("HTTP_errors/401.html", {"request": request})


async def cloudinary_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("HTTP_errors/501.html", {"request": request})


async def unprocessable_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("HTTP_errors/422.html", {"request": request})


async def subscribe_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("HTTP_errors/409.html", {"request": request})
