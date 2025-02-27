from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    __table_args__ = {"extend_existing": True}  # Добавлено


    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
    
    rooms = relationship("Rooms", back_populates="hotel")
    
    
    def __str__(self):
        return self.name


class Rooms(Base):
    __tablename__ = "rooms"  # комнаты
    __table_args__ = {"extend_existing": True}  # Добавлено


    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    hotel = relationship("Hotels", back_populates="rooms")
    booking = relationship("Bookings", back_populates="room")
    
    
    def __str__(self):
        return self.name