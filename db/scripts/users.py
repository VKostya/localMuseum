from fastapi import HTTPException, status
from pony.orm import db_session
from db.base import Users
from utils.security import Hasher


@db_session
def create_new_user(email, password, role_id=1, is_valid=0, send_notifications=0):
    Users(
        email=email,
        password=Hasher.get_password_hash(password),
    )


@db_session
def select_user_email(email):
    return Users.get(email=email)


@db_session
def update_notifications(id, value):
    Users[id].send_notifications = value


@db_session
def update_email(id, value):
    Users[id].email = value


@db_session
def update_pass(id, value):
    Users[id].password = Hasher.get_password_hash(value)


def user_is_admin(user: Users):
    if not user.role_id == 3:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
