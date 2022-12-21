from pydantic import BaseModel


class MuseumBase(BaseModel):
    title: str
    description: str
    address: str
    contact_url: str
    ticket_price: float
    schedule: str
    manager_id: int


class MuseumRead(MuseumBase):
    id: int
    image_url: str

    class Config:
        orm_mode = True
