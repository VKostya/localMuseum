from pony.orm import db_session
from db.base import Users
from utils.security import Hasher


@db_session
def create_new_user(email, password):
    Users(email=email, password=Hasher.get_password_hash(password))


@db_session
def select_user_email(email):
    return Users.get(email=email)


def user_is_admin(user: Users):
    return user.role_id == 3
