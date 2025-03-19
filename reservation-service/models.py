from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    member_id = Column(Integer, index=True)
    reservation_date = Column(DateTime, default=datetime.utcnow)
