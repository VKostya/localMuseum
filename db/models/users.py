from pony.orm import PrimaryKey, Required

from db.base import db


class Users(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str)
    role_id = Required(int)
    is_valid = Required(int)
    send_notifications = Required(int)


db.generate_mapping(create_tables=True)
