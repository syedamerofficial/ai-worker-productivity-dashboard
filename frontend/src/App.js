import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [workers, setWorkers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchWorkers(retry = 0) {
      try {
        const res = await axios.get(
          "https://ai-worker-dashboard-b6tl.onrender.com/metrics/workers"
        );

        setWorkers(res.data);
        setError("");
        setLoading(false);
      } catch (err) {
        console.log("Backend might be waking up...");

        if (retry < 4) {
          setTimeout(() => fetchWorkers(retry + 1), 4000);
        } else {
          setError(
            "Backend is waking up (Render free tier). Please refresh in a few seconds."
          );
          setLoading(false);
        }
      }
    }

    fetchWorkers();
  }, []);

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1 style={{ marginBottom: "20px" }}>
        Factory Productivity Dashboard v3
      </h1>

      <table
        border="1"
        cellPadding="10"
        style={{ borderCollapse: "collapse", width: "100%" }}
      >
        <thead style={{ backgroundColor: "#f2f2f2" }}>
          <tr>
            <th>Worker</th>
            <th>Active (sec)</th>
            <th>Idle (sec)</th>
            <th>Util %</th>
            <th>Units</th>
            <th>Units/hr</th>
          </tr>
        </thead>

        <tbody>
          {loading && (
            <tr>
              <td colSpan="6" style={{ textAlign: "center" }}>
                Loading data...
              </td>
            </tr>
          )}

          {!loading && error && (
            <tr>
              <td
                colSpan="6"
                style={{ color: "orange", textAlign: "center", fontWeight: "bold" }}
              >
                {error}
              </td>
            </tr>
          )}

          {!loading &&
            !error &&
            workers.map((w) => (
              <tr key={w.worker_id}>
                <td>{w.worker_id}</td>
                <td>{w.active_time_sec}</td>
                <td>{w.idle_time_sec}</td>
                <td>{w.utilization_pct}</td>
                <td>{w.units_produced}</td>
                <td>{w.units_per_hour}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;