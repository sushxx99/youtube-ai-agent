# 📺 YouTube AI Agent – MCP-Powered Intelligent Assistant

A full-stack, production-ready AI Agent that integrates with YouTube using the **Model Context Protocol (MCP)**.
The system enables natural-language interactions such as discovering videos, liking content, posting comments, managing playlists, and accessing user-specific data.
Built with **Next.js**, **FastAPI**, **MCP**, and **Google OAuth 2.0**, fully deployed on **Vercel (frontend)** and **Render (backend)**.

---

# 🎯 1. Project Overview

This project delivers an intelligent assistant capable of communicating with YouTube programmatically using conversational input.
A dedicated MCP server exposes YouTube API operations as standardized tools consumable by AI models.

Capabilities include:

* Natural-language video search and trending discovery
* Authenticated YouTube actions (likes, comments, subscriptions)
* Multi-turn contextual understanding
* Robust OAuth authentication
* Fully deployed, scalable, and secure architecture

---

# 🧩 2. Problem Statement

As part of the MCP Agent Development Assignment, the requirement was to design and deploy an AI agent that:

* Integrates with an external platform (YouTube)
* Wraps the platform’s API as MCP Tools
* Allows AI models to perform real actions through the MCP server
* Is fully deployed and publicly accessible
* Includes clear, professional documentation
* Must be completed within 48 hours

This project meets all assignment deliverables and evaluation criteria.

---

# ✔️ 3. How Requirements Are Fulfilled

| Requirement          | Implementation                                                   |
| -------------------- | ---------------------------------------------------------------- |
| Platform Integration | YouTube Data API v3 (OAuth + API key)                            |
| MCP Server           | FastAPI MCP engine exposing 22 standardized tools                |
| Agent Actions        | Search, trending, recommend, like, comment, subscribe, playlists |
| Architecture         | Full-stack, modular, clean                                       |
| Deployment           | Vercel (frontend), Render (backend)                              |
| Documentation        | Complete README + clear instructions                             |
| Time Constraint      | Delivered within the 48-hour assignment window                   |

---

# ⚙️ 4. Key Features

### 4.1 User Interaction

* Natural-language video search
* Automatic intent classification
* Multi-turn conversation memory
* Pagination and nextPageToken awareness
* Context-based recommendations

### 4.2 Authenticated YouTube Actions

* Like / Unlike
* Dislike (private feedback)
* Comment on videos
* Subscribe / Unsubscribe
* Playlist creation and management
* Fetch watch history, liked videos

### 4.3 System Capabilities

* Standardized MCP tool schemas
* Async YouTube client with retry logic
* Secure OAuth through HTTP-only cookies
* Fully responsive UI

---

# 🏗️ 5. System Architecture

```
                         User Browser
             (youtube-ai-agent-two.vercel.app)
                                │
                          HTTPS + Cookies
                                │
                        Next.js Frontend (Vercel)
        ┌───────────────────────────────────────────────────────┐
        │ UI (page.js) ─ Components (VideoCard, MessageBubble)   │
        │ Next.js API (/api/chat)                                │
        │ • Intent detection                                      │
        │ • Session/context management                            │
        │ • Calls MCP server                                      │
        └────────────────────────────────────────────────────────┘
                                │
                      POST /mcp/call (Fetch API)
                                │
                       FastAPI MCP Server (Render)
        ┌───────────────────────────────────────────────────────┐
        │ main.py        → FastAPI app, CORS, middleware         │
        │ mcp_server.py  → MCP tool schema + execution           │
        │ youtube_tools.py → YouTube Data API client             │
        │ oauth.py       → Google OAuth 2.0 flow                 │
        └────────────────────────────────────────────────────────┘
                                │
                     Google OAuth 2.0 and YouTube API
```

---

# 🧱 6. Technology Stack

### Frontend

* Next.js 14 (App Router)
* React, JavaScript
* Fetch API
* Vercel deployment

### Backend

* FastAPI
* Python 3.11
* Uvicorn
* httpx
* Render deployment

### External

* Google OAuth 2.0
* YouTube Data API v3
* Model Context Protocol

---

# 📁 7. Project Structure

```
youtube-ai-agent/
│
├── backend/
│   ├── main.py
│   ├── mcp_server.py
│   ├── oauth.py
│   ├── youtube_tools.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app/
│   │   ├── page.js
│   │   ├── layout.js
│   │   ├── globals.css
│   │   ├── api/chat/route.js
│   │   ├── oauth/login/route.js
│   │   └── oauth/callback/route.js
│   ├── components/
│   │   ├── MessageBubble.jsx
│   │   ├── VideoCard.jsx
│   │   └── Loader.jsx
│   ├── package.json
│   └── .env.local
│
└── README.md
```

---

# 🔧 8. Setup & Installation

### Prerequisites

* Node.js 18+
* Python 3.11+
* Git
* Google Cloud Console access
* YouTube Data API enabled

---

# 🔐 9. Google Cloud Setup

### 9.1 Create Project

### 9.2 Enable YouTube Data API v3

### 9.3 Create OAuth Credentials

Configure:

* User Type: External
* Scopes added:

  * youtube.force-ssl
  * youtube.readonly
  * openid, profile, email

Authorized Redirect URIs:

Local

```
http://localhost:8000/oauth/callback
```

Production

```
https://youtube-ai-agent-backend.onrender.com/oauth/callback
```

### 9.4 Create API Key

Restrict to YouTube Data API.

---

# 🖥️ 10. Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate  (Windows)
pip install -r requirements.txt
```

Create `.env`:

```
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8000/oauth/callback
YOUTUBE_API_KEY=...
FRONTEND_URL=http://localhost:3000
```

Run:

```
uvicorn main:app --reload --port 8000
```

---

# 💻 11. Frontend Setup

```
cd frontend
npm install
```

`.env.local`:

```
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:8000/mcp
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3000
```

Run:

```
npm run dev
```

---

# 🌐 12. Deployment

### 12.1 Frontend (Vercel)

* Root: `frontend`
* Environment variables:

```
NEXT_PUBLIC_MCP_SERVER_URL=https://youtube-ai-agent-backend.onrender.com/mcp
NEXT_PUBLIC_BACKEND_URL=https://youtube-ai-agent-backend.onrender.com
NEXT_PUBLIC_FRONTEND_URL=https://youtube-ai-agent-two.vercel.app
```

Live: [https://youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)

### 12.2 Backend (Render)

* Root: `backend`
* Build: `pip install -r requirements.txt`
* Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Live: [https://youtube-ai-agent-backend.onrender.com](https://youtube-ai-agent-backend.onrender.com)

---

# 🔌 13. API Endpoints

### FastAPI Server

| Endpoint          | Description        |
| ----------------- | ------------------ |
| `/`               | Root health check  |
| `/mcp/tools`      | List all MCP tools |
| `/mcp/call`       | Execute a tool     |
| `/oauth/login`    | Start OAuth        |
| `/oauth/callback` | Token exchange     |
| `/oauth/userinfo` | Get profile        |
| `/oauth/logout`   | Logout             |

### Next.js Backend

| Endpoint              | Description                      |
| --------------------- | -------------------------------- |
| `/api/chat`           | Intent detection + MCP execution |
| `/api/oauth/login`    | Redirect to backend              |
| `/api/oauth/callback` | Handle OAuth                     |

---

# 🛠️ 14. MCP Tools

Categories include:

* Discovery: search_videos, search_channels, trending_videos
* Details: video_details, channel_details
* Actions: like_video, dislike_video, comment_on_video
* Subscriptions: subscribe, unsubscribe, list subscriptions
* Playlists: create, add, remove, list playlists
* User Data: watch_history, my_channel, liked_videos

Total tools: **22**.

---

# ▶️ 15. Usage Flow

1. User opens frontend
2. Clicks "Connect YouTube"
3. Completes OAuth 2.0 login
4. Sends natural-language prompts
5. Next.js identifies intent
6. Calls MCP tool via backend
7. FastAPI executes YouTube API action
8. Results displayed via UI components

---

# ⚠️ 16. Limitations

* No persistent database
* No automatic token refresh
* Rate-limited by YouTube API
* Basic error messages for some edge cases

---

# 🚀 17. Future Enhancements

* Redis-based session storage
* Token refresh pipeline
* Semantic embeddings for more accurate search
* Video upload support
* Advanced UI/UX (themes, playlist builder, history viewer)

---

# 👤 18. Credits

* Developer: Sushma Srinivas
* YouTube Data API
* MCP Framework
* FastAPI + Next.js
* Deployment: Render + Vercel

---

# 🔗 19. Project Links

* Frontend: [https://youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)
* Backend: [https://youtube-ai-agent-backend.onrender.com](https://youtube-ai-agent-backend.onrender.com)
* GitHub: [https://github.com/sushxx99/youtube-ai-agent](https://github.com/sushxx99/youtube-ai-agent)


