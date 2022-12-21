from fastapi import APIRouter, Body, File, UploadFile, HTTPException
import cloudinary
import cloudinary.uploader
from config import config
from schemas.museums import MuseumRead, MuseumBase
from pony.orm import db_session, commit
from db.models.museum import Museums
from db.scripts.museums import select_with_id

router = APIRouter()
cloudinary.config(
    cloud_name=config.CLOUD_NAME,
    api_key=config.API_KEY,
    api_secret=config.API_SECRET,
)


@router.get("/", response_model=list[MuseumRead])
async def get_all_museums():
    with db_session:
        museums = Museums.select()
        result = [MuseumRead.from_orm(m) for m in museums]
    return result


@router.get("/{id}", response_model=MuseumRead)
async def get_museum_by_id(id: int):
    museum = select_with_id(id)
    if not museum:
        raise HTTPException(status_code=404, detail="Музей не найден")
    result = MuseumRead.from_orm(museum)
    return result


@router.post("/")
async def upload_image(
    title: str,
    description: str,
    address: str,
    contact_url: str,
    ticket_price: float,
    schedule: str,
    manager_id: int,
    file: UploadFile = File(...),
):
    try:
        file_store = await file.read()
        result = cloudinary.uploader.upload(file_store, public_id=title, overwite=True)
        url = result.get("url")
    except:
        raise HTTPException(status_code=501, detail="Unable to load image")
    with db_session:
        museum_added = Museums(
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
