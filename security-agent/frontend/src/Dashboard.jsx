// src/Dashboard.jsx
import { useEffect, useState } from "react";
import Card from "./components/Card";

export default function Dashboard({ mode, date }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    let url = "";
    const formattedDate = date.toISOString().slice(0, 10);

    switch (mode) {
      case "infra":
        url = `http://localhost:8000/infrastructure?date=${formattedDate}`;
        break;
      case "network":
        url = `http://localhost:8000/network?date=${formattedDate}`;
        break;
      case "security":
        url = `http://localhost:8000/security?date=${formattedDate}`;
        break;
    }

    fetch(url)
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => {
        console.error("Erro ao buscar dados:", err);
        setData(null);
      });
  }, [mode, date]);

  if (!data) return <p>Carregando dados...</p>;

  // Renderizar cards dependendo do modo
  const renderCards = () => {
    if (mode === "infra") {
    return (
        <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
        <Card
            title="CPU Usage"
            value={data.cpu?.percent !== undefined ? `${data.cpu.percent}%` : "N/A"}
        />
        <Card
            title="RAM Usage"
            value={data.memory?.percent !== undefined ? `${data.memory.percent}%` : "N/A"}
        />
        <Card
            title="Disk Usage"
            value={data.disk?.percent !== undefined ? `${data.disk.percent}%` : "N/A"}
        />
        <Card title="Top CPU Processes">
            {data.top_cpu_processes?.length > 0 ? (
            data.top_cpu_processes.map((proc, idx) => (
                <p key={idx}>
                {proc.name} ({proc.cpu_percent}%)
                </p>
            ))
            ) : (
            <p>N/A</p>
            )}
        </Card>
        </div>
    );
    }

    if (mode === "network") {
        return (
            <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
            <Card
                title="Bytes Sent"
                value={data.bytes_sent ? `${(data.bytes_sent / (1024 ** 2)).toFixed(2)} MB` : "N/A"}
            />
            <Card
                title="Bytes Received"
                value={data.bytes_recv ? `${(data.bytes_recv / (1024 ** 2)).toFixed(2)} MB` : "N/A"}
            />
            <Card
                title="Active Connections"
                value={data.active_connections?.length ?? 0}
            />

            {/* Extra: Top Remote IPs */}
            <Card title="Top Remote IPs">
                {data.top_ips?.length > 0 ? (
                    data.top_ips.map((ip, idx) => (
                    <p key={idx}>
                        {ip.remote_ip} ({ip.port}) - {ip.country}, {ip.city}
                    </p>
                    ))
                ) : (
                    <p>N/A</p>
                )}
            </Card>

            {/* Extra: Processes using most CPU */}
            <Card title="Top CPU Processes">
                {data.top_cpu_processes?.length > 0 ? (
                data.top_cpu_processes.map((proc, idx) => (
                    <p key={idx}>
                    {proc.name} (PID: {proc.pid}) - {proc.cpu_percent.toFixed(1)}%
                    </p>
                ))
                ) : (
                <p>N/A</p>
                )}
            </Card>
            </div>
        );
        }

    if (mode === "security") {
        if (!data) return <p>Loading Security Data...</p>;

        return (
            <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
            <Card title="Total Events" value={data.total_events ?? 0} />
            <Card title="Alerts Today" value={data.alerts_today ?? 0} />
            <Card title="Top IP">
                {data.top_ips?.length > 0 ? (
                data.top_ips.map((ip, idx) => (
                    <p key={idx}>{ip.ip} ({ip.attempts})</p>
                ))
                ) : (
                <p>N/A</p>
                )}
            </Card>
            </div>
        );
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: 20 }}>{mode.toUpperCase()} Dashboard</h2>
      {renderCards()}
    </div>
  );
}