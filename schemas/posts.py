from pydantic import BaseModel


class PostsRead(BaseModel):
    id: int
    message: str
    time_published: str
    museum_id: int

    class Config:
        orm_mode = True
