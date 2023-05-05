from fastapi import HTTPException, status
from pony.orm import db_session, delete
from db.base import Subscriptions


@db_session
def sub_exists(museum_id, user_id):
    sub = Subscriptions.select(
        lambda s: s.museum_id == museum_id and s.user_id == user_id
    )
    if sub:
        return True
    return False


@db_session
def add_sub(museum_id, user_id):
    Subscriptions(museum_id=museum_id, user_id=user_id)


@db_session
def del_sub(museum_id, user_id):
    delete(
        s for s in Subscriptions if (s.museum_id == museum_id and s.user_id == user_id)
    )
