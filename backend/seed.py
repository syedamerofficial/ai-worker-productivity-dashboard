from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import Worker, Workstation, Event


def seed_database(db: Session):
    # 🔹 Clear existing events (so reseed works cleanly)
    db.query(Event).delete()
    db.query(Worker).delete()
    db.query(Workstation).delete()
    db.commit()

    # -----------------------------
    # Create Workers
    # -----------------------------
    workers = [
        Worker(id="W1", name="Amit"),
        Worker(id="W2", name="Ravi"),
        Worker(id="W3", name="Sara"),
        Worker(id="W4", name="John"),
        Worker(id="W5", name="Neha"),
        Worker(id="W6", name="Imran"),
    ]

    # -----------------------------
    # Create Workstations
    # -----------------------------
    stations = [
        Workstation(id="S1", name="Assembly"),
        Workstation(id="S2", name="Packaging"),
        Workstation(id="S3", name="Quality"),
        Workstation(id="S4", name="Labeling"),
        Workstation(id="S5", name="Inspection"),
        Workstation(id="S6", name="Dispatch"),
    ]

    db.add_all(workers + stations)
    db.commit()

    # -----------------------------
    # Realistic worker patterns
    # (active_sec, idle_sec, units)
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
        station_id = f"S{idx+1}"
        t0 = base_time + timedelta(minutes=idx * 5)

        # working start
        events.append(
            Event(
                id=f"{wid}_working",
                timestamp=t0,
                worker_id=wid,
                workstation_id=station_id,
                event_type="working",
                confidence=0.95,
                count=1,
            )
        )

        # idle event
        events.append(
            Event(
                id=f"{wid}_idle",
                timestamp=t0 + timedelta(seconds=active),
                worker_id=wid,
                workstation_id=station_id,
                event_type="idle",
                confidence=0.92,
                count=1,
            )
        )

        # production event
        events.append(
            Event(
                id=f"{wid}_prod",
                timestamp=t0 + timedelta(seconds=active + idle),
                worker_id=wid,
                workstation_id=station_id,
                event_type="product_count",
                confidence=0.97,
                count=units,
            )
        )

    db.add_all(events)
    db.commit()