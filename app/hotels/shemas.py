from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int

    class Config:
        from_attributes = True


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int

    class Config:
        from_attributes = True
