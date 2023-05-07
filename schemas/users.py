from pydantic import BaseModel, validator
import re


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

    @validator("email")
    def check_if_email(cls, v):
        char_list = list(v)
        if not ("@" in char_list):
            return ValueError("not match")
        return v


class UserRead(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
