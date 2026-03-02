from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import hashlib

from .database import Base, engine, get_db
from .models import Event
from .schemas import EventIn
from .metrics import compute_worker_metrics
from .seed import seed_database

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Worker Productivity Dashboard")


# ⭐ AUTO-SEED ON STARTUP (IMPORTANT FIX)
@app.on_event("startup")
def auto_seed():
    db = next(get_db())
    seed_database(db)


def generate_event_id(event: EventIn):
    raw = (
        f"{event.timestamp}-{event.worker_id}-"
        f"{event.workstation_id}-{event.event_type}-{event.count}"
    )
    return hashlib.md5(raw.encode()).hexdigest()