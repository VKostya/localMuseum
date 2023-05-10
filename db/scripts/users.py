from fastapi import HTTPException, status
from pony.orm import db_session
from db.base import Subscriptions, Users
from schemas.users import UserRead
from utils.security import Hasher


@db_session
def create_new_user(email, password):
    Users(
        email=email,
        password=Hasher.get_password_hash(password),
    )


@db_session
def select_user_email(email):
    return Users.get(email=email)


@db_session
def get_email(id):
    return Users[id].email


@db_session
def update_notifications(id, value):
    Users[id].send_notifications = value


@db_session
def update_verif(id):
    Users[id].is_valid = 1


@db_session
def update_role(id, role_id):
    Users[id].role_id = role_id


@db_session
def update_email(id, value):
    Users[id].email = value
    Users[id].is_valid = 0


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


@db_session
def select_user_with_id(id):
    return Users.get(id=id)


@db_session
def get_subs_email(museum_id):
    users_list = []
    users_id = Subscriptions.select(lambda s: s.museum_id == museum_id)
    for u in users_id:
        users = Users.select(
            lambda us: us.id == u.user_id
            and us.is_valid == 1
            and us.send_notifications == 1
        )
        users_list.append([UserRead.from_orm(us) for us in users])
    users_mail = [u[0].email for u in users_list]
    return users_mail
