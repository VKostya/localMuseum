from fastapi import APIRouter, HTTPException
from schemas.museums import MuseumRead
from pony.orm import db_session
from db.base import Museums
from db.scripts.museums import select_with_id, validate_id

router = APIRouter()


@router.get("/", response_model=list[MuseumRead])
async def get_all_museums():
    with db_session:
        museums = Museums.select()
        result = [MuseumRead.from_orm(m) for m in museums]
    return result


@router.get("/{id}", response_model=MuseumRead)
async def get_museum_by_id(id: int):
    validate_id(id)
    museum = select_with_id(id)
    result = MuseumRead.from_orm(museum)
    return result
