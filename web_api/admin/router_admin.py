from fastapi import APIRouter, Body, Depends, File, UploadFile, HTTPException, status
import cloudinary
import cloudinary.uploader
from config import config
from pony.orm import db_session
from db.base import Museums, Users
from db.scripts.museums import (
    select_with_id,
    upgate_image_url,
    validate_id,
    update_sql_data,
    delete_with_id,
)
from db.scripts.users import user_is_admin
from schemas.museums import MuseumBase
from utils.cloudinary_utils import load_to_cloudinary
from web_api.auth.router_auth import get_current_user_from_token

cloudinary.config(
    cloud_name=config.CLOUD_NAME,
    api_key=config.API_KEY,
    api_secret=config.API_SECRET,
)

router = APIRouter()


@router.post("/museum")
async def create_museum(
    title: str,
    description: str,
    address: str,
    contact_url: str,
    ticket_price: float,
    schedule: str,
    manager_id: int,
    file: UploadFile = File(...),
    current_user: Users = Depends(get_current_user_from_token),
):
    user_is_admin(current_user)

    try:
        url = await load_to_cloudinary(title, file)
    except:
        raise HTTPException(status_code=501, detail="Unable to load image")
    with db_session:
        Museums(
            title=title,
            image_url=url,
            description=description,
            address=address,
            contact_url=contact_url,
            ticket_price=ticket_price,
            schedule=schedule,
            manager_id=manager_id,
        )
    return {"result": "OK"}


@router.patch("/museum/image/{id}")
async def update_image(
    id: int,
    file: UploadFile = File(...),
    current_user: Users = Depends(get_current_user_from_token),
):
    user_is_admin(current_user)
    validate_id(id)
    museum = select_with_id(id)
    try:
        url = load_to_cloudinary(museum.title, file)
    except:
        raise HTTPException(status_code=501, detail="Unable to load image")

    upgate_image_url(id, url)
    return {"result": "ok"}


@router.patch("/museum/{id}")
async def update_info(
    id: int,
    data: MuseumBase = Body(...),
    current_user: Users = Depends(get_current_user_from_token),
):
    user_is_admin(current_user)
    validate_id(id)
    update_sql_data(id, data)
    return {"result": "ok"}


@router.delete("/museum/{id}")
async def delete_museum(
    id: int, current_user: Users = Depends(get_current_user_from_token)
):
    user_is_admin(current_user)
    validate_id(id)
    delete_with_id(id)
    return {"result": "ok"}
