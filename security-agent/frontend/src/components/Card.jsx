export default function Card({ title, value, children }) {
  return (
    <div style={{
      border: "1px solid #ccc",
      borderRadius: 8,
      padding: 20,
      minWidth: 200,
      boxShadow: "2px 2px 12px rgba(0,0,0,0.1)"
    }}>
      <h3>{title}</h3>
      {value !== undefined ? <p>{value}</p> : children}
    </div>
  );
}