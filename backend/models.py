from sqlalchemy import Column, String, Float, Integer, DateTime
from .database import Base


class Worker(Base):
    __tablename__ = "workers"
    worker_id = Column(String, primary_key=True)
    name = Column(String)


class Workstation(Base):
    __tablename__ = "workstations"
    station_id = Column(String, primary_key=True)
    name = Column(String)


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, index=True)
    worker_id = Column(String, index=True)
    workstation_id = Column(String, index=True)
    event_type = Column(String)
    confidence = Column(Float)
    count = Column(Integer, default=0)
