from datetime import datetime, timedelta
from .models import Worker, Workstation, Event
import hashlib


def generate_id(raw: str):
    return hashlib.md5(raw.encode()).hexdigest()


def seed_database(db):
    db.query(Event).delete()
    db.query(Worker).delete()
    db.query(Workstation).delete()

    for i in range(1, 7):
        db.add(Worker(worker_id=f"W{i}", name=f"Worker {i}"))

    for i in range(1, 7):
        db.add(Workstation(station_id=f"S{i}", name=f"Station {i}"))

    base_time = datetime.utcnow() - timedelta(hours=2)

    for i in range(1, 7):
        wid = f"W{i}"
        sid = f"S{i}"

        events = [
            ("working", 0, 0),
            ("product_count", 10, 30),
            ("idle", 0, 60),
            ("working", 0, 90),
            ("product_count", 5, 120),
        ]

        for etype, count, offset in events:
            ts = base_time + timedelta(seconds=offset)
            raw = f"{wid}-{sid}-{ts}-{etype}-{count}"
            db.add(
                Event(
                    id=generate_id(raw),
                    timestamp=ts,
                    worker_id=wid,
                    workstation_id=sid,
                    event_type=etype,
                    confidence=0.95,
                    count=count,
                )
            )

    db.commit()
