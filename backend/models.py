from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    itinerary = relationship("Itinerary", back_populates="user", uselist=False)

class Itinerary(Base):
    __tablename__ = 'itineraries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    user = relationship("User", back_populates="itinerary")
    days = relationship("Day", back_populates="itinerary", cascade="all, delete-orphan")

class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey('itineraries.id'), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(String(20), nullable=True)
    start_location = Column(String(200), nullable=False)
    end_location = Column(String(200), nullable=False)
    distance_km = Column(Float, nullable=False)
    lodging_info = Column(Text, default="")
    notes = Column(Text, default="")
    polyline = Column(Text, default="")  # JSON string with list of {lat, lng}
    itinerary = relationship("Itinerary", back_populates="days")
    pois = relationship("POI", back_populates="day", cascade="all, delete-orphan")

class POI(Base):
    __tablename__ = 'pois'
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey('days.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    category = Column(String(50), default="geral")
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    day = relationship("Day", back_populates="pois")
