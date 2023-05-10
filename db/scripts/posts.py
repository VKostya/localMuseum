from fastapi import HTTPException
from pony.orm import db_session, commit, select, delete
from db.base import Museums, Subscriptions, Posts
from schemas.museums import MuseumBase
from schemas.posts import PostsRead


@db_session
def delete_message_with_id(id):
    Posts[id].delete()
    commit()


@db_session
def add_post(text, date, id):
    Posts(message=text, time_published=date, museum_id=id)


@db_session
def select_museum_posts(id):
    posts = Posts.select(lambda m: m.museum_id == id)
    return [PostsRead.from_orm(p) for p in posts]
