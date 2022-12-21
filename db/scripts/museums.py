from pony.orm import db_session

from db.models.museum import Museums


@db_session
def select_with_id(id):
    return Museums.get(id=id)
