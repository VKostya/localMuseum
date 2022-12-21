from fastapi import HTTPException
from pony.orm import db_session, commit
from db.base import Museums
from schemas.museums import MuseumBase


@db_session
def select_with_id(id):
    return Museums.get(id=id)


@db_session
def upgate_image_url(id, url):
    Museums[id].image_url = url


@db_session
def update_sql_data(id, data: MuseumBase):
    Museums[id].title = data.title
    Museums[id].description = data.description
    Museums[id].address = data.address
    Museums[id].contact_url = data.contact_url
    Museums[id].ticket_price = data.ticket_price
    Museums[id].schedule = data.schedule
    Museums[id].manager_id = data.manager_id


@db_session
def delete_with_id(id):
    Museums[id].delete()
    commit()


def validate_id(id):
    museum = select_with_id(id)
    if not museum:
        raise HTTPException(status_code=404, detail="Музей не найден")
