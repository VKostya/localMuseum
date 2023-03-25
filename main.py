import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from config import config
from web_api.base import api_router
from web_app.base import app_router
from utils.exception_handlers import (
    not_found_error,
    not_authenticated_error,
    cloudinary_error,
    subscribe_error,
    unprocessable_error,
)

exception_handlers = {
    404: not_found_error,
    401: not_authenticated_error,
    409: subscribe_error,
    422: unprocessable_error,
    501: cloudinary_error,
}
app = FastAPI(exception_handlers=exception_handlers)

app.include_router(api_router, prefix="/api")
app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
