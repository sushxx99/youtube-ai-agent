export default function MessageBubble({ role, text }) {
  const isUser = role === "user";
  
  return (
    <div style={{
      display: "flex",
      justifyContent: isUser ? "flex-end" : "flex-start",
      marginBottom: "16px",
      animation: "slideIn 0.3s ease-out"
    }}>
      <div style={{
        maxWidth: "75%",
        padding: "14px 18px",
        borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
        background: isUser 
          ? "linear-gradient(135deg, #ff0000 0%, #cc0000 100%)" 
          : "rgba(255,255,255,0.08)",
        border: isUser ? "none" : "1px solid rgba(255,255,255,0.1)",
        color: "white",
        fontSize: "15px",
        lineHeight: "1.5",
        fontWeight: "400",
        boxShadow: isUser 
          ? "0 4px 12px rgba(255,0,0,0.2)" 
          : "none"
      }}>
        {text}
      </div>
      <style jsx>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}