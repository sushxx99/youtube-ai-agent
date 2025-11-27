"use client";

import { useState, useRef, useEffect } from "react";
import MessageBubble from "../components/MessageBubble";
import VideoCard from "../components/VideoCard";
import Loader from "../components/Loader";

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  // Backend base URL (example: https://youtube-ai-agent-backend.onrender.com)
  const BACKEND_URL = process.env.NEXT_PUBLIC_MCP_SERVER_URL.replace("/mcp", "");

  useEffect(() => {
    fetchUser();
  }, []);

  async function fetchUser() {
  try {
    const res = await fetch(`${BACKEND_URL}/oauth/userinfo`, {
      credentials: "include",
    });
    const data = await res.json();

    if (data.logged_in) {
      setUser(data.profile);

      // 🔥 Fetch backend token & store it
      const tokenRes = await fetch(`${BACKEND_URL}/oauth/token`, {
        credentials: "include",
      });
      const tokenData = await tokenRes.json();

      if (tokenData.token) {
        localStorage.setItem("yt_access_token", tokenData.token);
        console.log("✅ Token saved to localStorage");
      }
    }
  } catch (err) {}
}


  async function sendMessage() {
  if (!input.trim() || loading) return;

  const userMsg = input;
  setInput("");
  setLoading(true);

  setMessages(prev => [...prev, { role: "user", text: userMsg }]);

  try {
    // 🔥 Retrieve token from localStorage
    const token = localStorage.getItem("yt_access_token");

    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": token ? `Bearer ${token}` : ""
      },
      body: JSON.stringify({ message: userMsg }),
    });

    const data = await res.json();

    if (data.type === "tool_result" && data.data?.data?.items) {
      setMessages(prev => [
        ...prev,
        { role: "assistant", text: data.reply },
        { role: "videos", videos: data.data.data.items }
      ]);
    } else {
      setMessages(prev => [...prev, { role: "assistant", text: data.reply }]);
    }
  } catch (err) {
    setMessages(prev => [...prev, { role: "assistant", text: "⚠️ Connection error" }]);
  } finally {
    setLoading(false);
  }
}


  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading]);

  const suggestions = [
    "python tutorials",
    "trending videos", 
    "best tech channels",
    "recommend the best"
  ];

  return (
    <main style={{
      height: "100vh",
      display: "flex",
      flexDirection: "column",
      background: "#0f0f0f",
      fontFamily: "system-ui, -apple-system, sans-serif"
    }}>
      <header style={{
        padding: "16px 32px",
        background: "rgba(24,24,24,0.95)",
        backdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(255,255,255,0.08)",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        position: "sticky",
        top: 0,
        zIndex: 100
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div style={{
            width: "40px",
            height: "40px",
            background: "linear-gradient(135deg, #ff0000 0%, #cc0000 100%)",
            borderRadius: "12px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "24px"
          }}>▶</div>
          <div>
            <h1 style={{ 
              margin: 0, 
              fontSize: "20px", 
              fontWeight: "600",
              color: "white"
            }}>
              YouTube AI Agent
            </h1>
            <p style={{ margin: "2px 0 0", fontSize: "13px", color: "rgba(255,255,255,0.5)" }}>
              Powered by MCP
            </p>
          </div>
        </div>

        {user ? (
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: "14px", fontWeight: "500", color: "white" }}>
                {user.name}
              </div>
              <div style={{ fontSize: "12px", color: "rgba(255,255,255,0.5)" }}>
                Connected
              </div>
            </div>

            <img src={user.picture} alt="avatar" style={{
              width: "40px",
              height: "40px",
              borderRadius: "50%",
              border: "2px solid rgba(255,255,255,0.2)"
            }} />

            {/* LOGOUT BUTTON */}
            <button
              onClick={() =>
                window.location.href = `${BACKEND_URL}/oauth/logout`
              }
              style={{
                background: "rgba(255,255,255,0.1)",
                color: "white",
                padding: "8px 16px",
                borderRadius: "8px",
                border: "1px solid rgba(255,255,255,0.1)",
                cursor: "pointer",
                fontSize: "14px",
                fontWeight: "500",
                transition: "all 0.2s"
              }}
              onMouseEnter={e => e.target.style.background = "rgba(255,255,255,0.15)"}
              onMouseLeave={e => e.target.style.background = "rgba(255,255,255,0.1)"}
            >
              Logout
            </button>

          </div>
        ) : (
          /* LOGIN BUTTON */
          <button
            onClick={() =>
              window.location.href = `${BACKEND_URL}/oauth/login`
            }
            style={{
              background: "#ff0000",
              color: "white",
              padding: "10px 24px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              fontWeight: "600",
              fontSize: "14px",
              transition: "all 0.2s"
            }}
            onMouseEnter={e => e.target.style.transform = "scale(1.05)"}
            onMouseLeave={e => e.target.style.transform = "scale(1)"}
          >
            Connect YouTube
          </button>
        )}
      </header>


      <div ref={scrollRef} style={{
        flex: 1,
        overflowY: "auto",
        padding: "32px",
        maxWidth: "1200px",
        width: "100%",
        margin: "0 auto"
      }}>
        {messages.length === 0 && (
          <div style={{
            textAlign: "center",
            marginTop: "80px"
          }}>
            <div style={{
              fontSize: "48px",
              marginBottom: "16px"
            }}>🎬</div>
            <h2 style={{ 
              fontSize: "32px", 
              marginBottom: "12px",
              color: "white",
              fontWeight: "600"
            }}>
              Your YouTube AI Assistant
            </h2>
            <p style={{ 
              fontSize: "16px", 
              color: "rgba(255,255,255,0.6)",
              marginBottom: "32px"
            }}>
              Search videos, get recommendations, or perform actions
            </p>

            <div style={{
              display: "flex",
              gap: "12px",
              justifyContent: "center",
              flexWrap: "wrap"
            }}>
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  onClick={() => setInput(s)}
                  style={{
                    background: "rgba(255,255,255,0.05)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    color: "rgba(255,255,255,0.8)",
                    padding: "10px 20px",
                    borderRadius: "20px",
                    cursor: "pointer",
                    fontSize: "14px",
                    transition: "all 0.2s"
                  }}
                  onMouseEnter={e => {
                    e.target.style.background = "rgba(255,255,255,0.1)";
                    e.target.style.borderColor = "rgba(255,255,255,0.2)";
                  }}
                  onMouseLeave={e => {
                    e.target.style.background = "rgba(255,255,255,0.05)";
                    e.target.style.borderColor = "rgba(255,255,255,0.1)";
                  }}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => {
          if (msg.role === "videos") {
            return (
              <div key={i} style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
                gap: "20px",
                marginTop: "20px"
              }}>
                {msg.videos.map((v, idx) => <VideoCard key={idx} item={v} />)}
              </div>
            );
          }
          return <MessageBubble key={i} role={msg.role} text={msg.text} />;
        })}

        {loading && <Loader />}
      </div>

      <div style={{
        padding: "20px 32px 32px",
        background: "rgba(24, 24, 24, 0.95)",
        backdropFilter: "blur(20px)",
        borderTop: "1px solid rgba(255,255,255,0.08)",
        maxWidth: "1200px",
        width: "100%",
        margin: "0 auto"
      }}>
        <div style={{ display: "flex", gap: "12px" }}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && sendMessage()}
            placeholder="Search videos, get recommendations, or ask me to like/comment..."
            disabled={loading}
            style={{
              flex: 1,
              padding: "16px 20px",
              borderRadius: "12px",
              border: "1px solid rgba(255,255,255,0.1)",
              background: "rgba(255,255,255,0.05)",
              fontSize: "15px",
              outline: "none",
              color: "white",
              transition: "all 0.2s"
            }}
            onFocus={e => {
              e.target.style.borderColor = "rgba(255,255,255,0.2)";
              e.target.style.background = "rgba(255,255,255,0.08)";
            }}
            onBlur={e => {
              e.target.style.borderColor = "rgba(255,255,255,0.1)";
              e.target.style.background = "rgba(255,255,255,0.05)";
            }}
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            style={{
              padding: "16px 32px",
              borderRadius: "12px",
              background: loading ? "rgba(255,255,255,0.1)" : "#ff0000",
              color: "white",
              border: "none",
              cursor: loading ? "not-allowed" : "pointer",
              fontWeight: "600",
              fontSize: "15px",
              transition: "all 0.2s"
            }}
            onMouseEnter={e => !loading && (e.target.style.background = "#cc0000")}
            onMouseLeave={e => !loading && (e.target.style.background = "#ff0000")}>
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </main>
  );
}