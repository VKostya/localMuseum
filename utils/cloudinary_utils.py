import cloudinary
import cloudinary.uploader
from fastapi import File, HTTPException, UploadFile
from config import config

cloudinary.config(
    cloud_name=config.CLOUD_NAME,
    api_key=config.API_KEY,
    api_secret=config.API_SECRET,
)


async def load_to_cloudinary(title: str, file: UploadFile = File(...)):
    try:
        file_store = await file.read()
        result = cloudinary.uploader.upload(file_store, public_id=title, overwite=True)
        return result.get("url")
    except:
        raise HTTPException(status_code=501, detail="Unable to load image")
