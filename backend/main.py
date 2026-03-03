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


# ✅ AUTO-SEED ON STARTUP
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


# -------------------------------
# ROUTES (YOU ACCIDENTALLY REMOVED THESE)
# -------------------------------

@app.post("/ingest")
def ingest_event(event: EventIn, db: Session = Depends(get_db)):
    eid = generate_event_id(event)

    exists = db.query(Event).filter(Event.id == eid).first()
    if exists:
        return {"status": "duplicate ignored"}

    db.add(
        Event(
            id=eid,
            timestamp=event.timestamp,
            worker_id=event.worker_id,
            workstation_id=event.workstation_id,
            event_type=event.event_type,
            confidence=event.confidence,
            count=event.count,
        )
    )
    db.commit()
    return {"status": "ingested"}


@app.get("/metrics/workers")
def worker_metrics(db: Session = Depends(get_db)):
    return compute_worker_metrics(db)


@app.post("/seed")
def seed(db: Session = Depends(get_db)):
    seed_database(db)
    return {"status": "database seeded"}