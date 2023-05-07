from fastapi import HTTPException
from pony.orm import db_session, commit, select, delete
from db.base import Verifications
from db.scripts.users import update_verif


@db_session
def check_ver_attempt(user_id):
    return not (Verifications.get(user_id=user_id))


@db_session
def add_verification_pair(user_id, hash_code):
    Verifications(user_id=user_id, hash_code=hash_code)


@db_session
def correct_hash(hash):
    return Verifications.get(hash_code=hash)


@db_session
def verif_pair(user_id, hash_code):
    ver = Verifications.get(hash_code=hash_code)
    return ver.user_id == user_id


@db_session
def remove_verif_pair(hash_id):
    ver = Verifications.get(hash_code=hash_id)
    update_verif(ver.user_id)
    delete(v for v in Verifications if (v.hash_code == hash_id))
