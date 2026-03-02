from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import Worker, Workstation, Event


def seed_database(db: Session):
    # clear old data
    db.query(Event).delete()
    db.query(Worker).delete()
    db.query(Workstation).delete()
    db.commit()

    # -----------------------------
    # Workers
    # -----------------------------
    workers = [
        Worker(worker_id="W1", name="Amit"),
        Worker(worker_id="W2", name="Ravi"),
        Worker(worker_id="W3", name="Sara"),
        Worker(worker_id="W4", name="John"),
        Worker(worker_id="W5", name="Neha"),
        Worker(worker_id="W6", name="Imran"),
    ]

    # -----------------------------
    # Workstations
    # -----------------------------
    stations = [
        Workstation(station_id="S1", name="Assembly"),
        Workstation(station_id="S2", name="Packaging"),
        Workstation(station_id="S3", name="Quality"),
        Workstation(station_id="S4", name="Labeling"),
        Workstation(station_id="S5", name="Inspection"),
        Workstation(station_id="S6", name="Dispatch"),
    ]

    db.add_all(workers + stations)
    db.commit()

    # -----------------------------
    # realistic patterns
    # -----------------------------
    patterns = {
        "W1": (60, 30, 10),
        "W2": (120, 20, 15),
        "W3": (90, 40, 8),
        "W4": (150, 10, 22),
        "W5": (80, 50, 6),
        "W6": (110, 25, 12),
    }

    base_time = datetime.utcnow()
    events = []

    for idx, (wid, (active, idle, units)) in enumerate(patterns.items()):
        sid = f"S{idx+1}"
        t0 = base_time + timedelta(minutes=idx * 5)

        events.append(
            Event(
                id=f"{wid}_working",
                timestamp=t0,
                worker_id=wid,
                workstation_id=sid,
                event_type="working",
                confidence=0.95,
                count=1,
            )
        )

        events.append(
            Event(
                id=f"{wid}_idle",
                timestamp=t0 + timedelta(seconds=active),
                worker_id=wid,
                workstation_id=sid,
                event_type="idle",
                confidence=0.92,
                count=1,
            )
        )

        events.append(
            Event(
                id=f"{wid}_prod",
                timestamp=t0 + timedelta(seconds=active + idle),
                worker_id=wid,
                workstation_id=sid,
                event_type="product_count",
                confidence=0.97,
                count=units,
            )
        )

    db.add_all(events)
    db.commit()