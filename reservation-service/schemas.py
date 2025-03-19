from pydantic import BaseModel
from datetime import datetime

class ReservationBase(BaseModel):
    book_id: int
    member_id: int

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    reservation_date: datetime

    class Config:
        orm_mode = True
