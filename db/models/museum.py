from pony.orm import PrimaryKey, Required

from db.base import db


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


db.generate_mapping(create_tables=True)
