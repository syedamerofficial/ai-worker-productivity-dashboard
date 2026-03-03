from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import hashlib

from .database import Base, engine, get_db
from .models import Event
from .schemas import EventIn
from .metrics import compute_worker_metrics
from .seed import seed_database

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Worker Productivity Dashboard")

# ✅ CORS (VERY IMPORTANT for Vercel frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all domains (safe for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Auto seed database on startup
@app.on_event("startup")
def auto_seed():
    db = next(get_db())
    seed_database(db)


# Generate unique event ID
def generate_event_id(event: EventIn):
    raw = (
        f"{event.timestamp}-{event.worker_id}-"
        f"{event.workstation_id}-{event.event_type}-{event.count}"
    )
    return hashlib.md5(raw.encode()).hexdigest()


# -------------------------------
# ROUTES
# -------------------------------

@app.post("/ingest")
def ingest_event(event: EventIn, db: Session = Depends(get_db)):
    event_id = generate_event_id(event)

    existing = db.query(Event).filter(Event.id == event_id).first()
    if existing:
        return {"status": "duplicate ignored"}

    new_event = Event(
        id=event_id,
        timestamp=event.timestamp,
        worker_id=event.worker_id,
        workstation_id=event.workstation_id,
        event_type=event.event_type,
        confidence=event.confidence,
        count=event.count,
    )

    db.add(new_event)
    db.commit()

    return {"status": "ingested"}


@app.get("/metrics/workers")
def worker_metrics(db: Session = Depends(get_db)):
    return compute_worker_metrics(db)


@app.post("/seed")
def seed(db: Session = Depends(get_db)):
    seed_database(db)
    return {"status": "database seeded"}