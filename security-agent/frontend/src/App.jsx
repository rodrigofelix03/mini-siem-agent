// src/App.jsx
import { useState } from "react";
import Dashboard from "./Dashboard";

function App() {
  const [mode, setMode] = useState("infra");
  const [date, setDate] = useState(new Date());

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif", background: "#121212", color: "white", minHeight: "100vh" }}>
      <h1>🛡 Mini SIEM Dashboard</h1>

      <div style={{ marginBottom: 20 }}>
        <button onClick={() => setMode("security")}>🛡 Security</button>
        <button onClick={() => setMode("infra")}>💻 Infra</button>
        <button onClick={() => setMode("network")}>🌐 Network</button>

        <input
          type="date"
          value={date.toISOString().slice(0, 10)}
          onChange={(e) => setDate(new Date(e.target.value))}
          style={{ marginLeft: 10 }}
        />
      </div>

      <Dashboard mode={mode} date={date} />
    </div>
  );
}

export default App;