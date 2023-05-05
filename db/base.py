from config import config
from pony.orm import Database, sql_debug, PrimaryKey, Required


db = Database()
db.bind(provider=config.DB_PROVIDER, filename=config.DB_NAME, create_db=True)


class Museums(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    image_url = Required(str)
    description = Required(str)
    address = Required(str)
    contact_url = Required(str)
    ticket_price = Required(float)
    schedule = Required(str)
    manager_id = Required(int)


class Users(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str)
    role_id = Required(int, default=1)
    is_valid = Required(int, default=0)
    send_notifications = Required(int, default=0)


class Subscriptions(db.Entity):
    id = PrimaryKey(int, auto=True)
    museum_id = Required(int)
    user_id = Required(int)


class Roles(db.Entity):
    id = PrimaryKey(int, auto=True)
    role = Required(str)


class Verifications(db.Entity):
    user_id = Required(int)
    hash_code = Required(str)


if config.DEBUG:
    sql_debug(True)

db.generate_mapping(create_tables=True)
