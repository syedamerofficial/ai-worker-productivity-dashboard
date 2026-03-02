from collections import defaultdict
from .models import Event


def compute_worker_metrics(db):
    events = db.query(Event).order_by(Event.worker_id, Event.timestamp).all()

    worker_stats = defaultdict(
        lambda: {"active": 0, "idle": 0, "units": 0}
    )

    # -----------------------------
    # time calculation (pairwise)
    # -----------------------------
    for i in range(len(events) - 1):
        curr = events[i]
        nxt = events[i + 1]

        if curr.worker_id != nxt.worker_id:
            continue

        duration = (nxt.timestamp - curr.timestamp).total_seconds()

        if curr.event_type == "working":
            worker_stats[curr.worker_id]["active"] += duration
        elif curr.event_type == "idle":
            worker_stats[curr.worker_id]["idle"] += duration

    # ⭐ IMPORTANT FIX — count ALL product events
    for e in events:
        if e.event_type == "product_count":
            worker_stats[e.worker_id]["units"] += e.count or 0

    # -----------------------------
    # build results
    # -----------------------------
    results = []
    for wid, s in worker_stats.items():
        total = s["active"] + s["idle"]
        util = (s["active"] / total * 100) if total else 0
        uph = s["units"] / (s["active"] / 3600) if s["active"] else 0

        results.append(
            {
                "worker_id": wid,
                "active_time_sec": round(s["active"], 2),
                "idle_time_sec": round(s["idle"], 2),
                "utilization_pct": round(util, 2),
                "units_produced": s["units"],
                "units_per_hour": round(uph, 2),
            }
        )

    return results