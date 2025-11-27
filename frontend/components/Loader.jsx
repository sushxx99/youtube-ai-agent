export default function Loader() {
  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      gap: "8px",
      padding: "12px 16px",
      marginBottom: "16px"
    }}>
      <div style={{
        width: "8px",
        height: "8px",
        borderRadius: "50%",
        background: "#2563eb",
        animation: "bounce 1.4s infinite ease-in-out"
      }} />
      <div style={{
        width: "8px",
        height: "8px",
        borderRadius: "50%",
        background: "#2563eb",
        animation: "bounce 1.4s infinite ease-in-out 0.2s"
      }} />
      <div style={{
        width: "8px",
        height: "8px",
        borderRadius: "50%",
        background: "#2563eb",
        animation: "bounce 1.4s infinite ease-in-out 0.4s"
      }} />
      <style jsx>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-10px); }
        }
      `}</style>
    </div>
  );
}