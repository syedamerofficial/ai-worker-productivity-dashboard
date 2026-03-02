import React, { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [workers, setWorkers] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const res = await axios.get("http://localhost:8000/metrics/workers");
    setWorkers(res.data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Factory Productivity Dashboard</h1>

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
          {workers.map((w) => (
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
