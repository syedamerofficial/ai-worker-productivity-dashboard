import React from "react";
import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [workers, setWorkers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchWorkers() {
      try {
        const res = await axios.get(
          "https://ai-worker-dashboard-b6tl.onrender.com/metrics/workers"
        );
        console.log("API DATA:", res.data);
        setWorkers(res.data);
      } catch (err) {
        console.error("FETCH ERROR:", err);
        setError("Failed to load data");
      } finally {
        setLoading(false);
      }
    }

    fetchWorkers();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Factory Productivity Dashboard v3</h1>

      <table border="1" cellPadding="8">
        <thead>
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
              <td colSpan="6">Loading...</td>
            </tr>
          )}

          {!loading && error && (
            <tr>
              <td colSpan="6" style={{ color: "red" }}>
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