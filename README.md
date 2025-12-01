# 📺 YouTube AI Agent – MCP-Powered Intelligent Assistant

A full-stack, production-ready AI Agent that integrates with **YouTube** using the **Model Context Protocol (MCP)**.
The system enables conversational interaction with YouTube — including video search, trending content, likes, comments, subscriptions, playlist management, and retrieval of user-specific data.

Built using:

* **Next.js 14 (App Router)** – Frontend (Vercel)
* **FastAPI + MCP Server** – Backend (Render)
* **Google OAuth 2.0** – Authentication
* **YouTube Data API v3** – Platform Integration

Fully deployed and publicly accessible.

---

# 🎯 1. Project Overview

This project provides an intelligent AI Assistant capable of executing real YouTube actions based on natural-language instructions.

The MCP server exposes YouTube functionalities as standardized tools, enabling the agent to:

* Search for videos
* Fetch trending content
* Like / Unlike / Dislike videos
* Comment on videos
* Subscribe / Unsubscribe from channels
* Create, update, and browse playlists
* Retrieve liked videos & watch history
* Make contextual recommendations
* Handle pagination (next page / more)
* Maintain conversation context

The entire project follows a clean, modular, and scalable architecture suitable for production use.

---

# 🧩 2. Problem Statement (Assignment Requirement)

Build and deploy an AI Agent that:

* Integrates with an external platform (YouTube)
* Exposes the platform's functionality as **MCP Tools**
* Allows the agent to perform real actions
* Uses any LLM provider / framework
* Is completely deployed and publicly accessible
* Includes professional engineering documentation
* Completed within a 48-hour window

This project satisfies **all** assignment deliverables and evaluation criteria.

---

# ✔️ 3. How Requirements Are Fulfilled

| Requirement           | Implementation                                 |
| --------------------- | ---------------------------------------------- |
| Platform Integration  | YouTube Data API v3 via OAuth2                 |
| MCP Server            | FastAPI MCP engine exposing 22 tools           |
| Authenticated Actions | Likes, comments, subscriptions, playlists      |
| Architecture          | Full-stack (Next.js + FastAPI), clean, modular |
| Live Deployment       | Vercel (frontend) + Render (backend)           |
| Documentation         | Complete README + architecture                 |
| Time Constraint       | Delivered within 48 hours                      |

---

# ⚙️ 4. Key Features

## 4.1 User Interaction

* Natural-language video search
* Trending video discovery
* Automatic intent classification
* Multi-turn contextual memory
* Pagination using nextPageToken
* Context-based recommendations

## 4.2 Authenticated YouTube Actions

* Like / Unlike
* Dislike
* Comment on videos
* Subscribe / Unsubscribe
* Playlist creation and management
* View watch history
* View liked videos

## 4.3 System-Level Capabilities

* Standardized MCP tool schemas
* Async YouTube client with retry logic
* Secure OAuth using HTTP-only cookies
* Fully responsive UI
* Error handling & fallback messages

---

# 🏗 5. System Architecture

```
                           User Browser
               (youtube-ai-agent-two.vercel.app)
                                   │
                             HTTPS + Cookies
                                   │
                        Next.js Frontend (Vercel)
        ┌────────────────────────────────────────────────────────┐
        │ UI (page.js)                                           │
        │ Components: MessageBubble, VideoCard, Loader           │
        │ Next.js API (/api/chat):                               │
        │  • Intent detection                                    │
        │  • Session/context management                          │
        │  • Requests MCP server                                 │
        └────────────────────────────────────────────────────────┘
                                   │
                         POST /mcp/call (tool requests)
                                   │
                         FastAPI MCP Server (Render)
        ┌────────────────────────────────────────────────────────┐
        │ main.py           – FastAPI app, CORS, middleware      │
        │ mcp_server.py     – MCP registry + tool executor       │
        │ youtube_tools.py  – YouTube Data API client wrappers   │
        │ oauth.py          – Google OAuth 2.0 flow              │
        └────────────────────────────────────────────────────────┘
                                   │
                       Google OAuth 2.0 + YouTube API v3
```

---

# 🧱 6. Technology Stack

### **Frontend**

* Next.js 14
* React
* JavaScript
* Fetch API
* Deployed on Vercel

### **Backend**

* FastAPI
* Python 3.11
* httpx
* Uvicorn
* Deployed on Render

### **External**

* Google OAuth 2.0
* YouTube Data API v3
* Model Context Protocol

---

# 📁 7. Project Structure (Clean + Matches Your Screenshot)

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
└── frontend/
    ├── app/
    │   ├── page.js
    │   ├── layout.js
    │   ├── global.css
    │   ├── api/
    │   │   └── chat/route.js
    │   └── oauth/
    │       ├── login/route.js
    │       └── callback/route.js
    │
    ├── components/
    │   ├── MessageBubble.jsx
    │   ├── VideoCard.jsx
    │   └── Loader.jsx
    │
    ├── package.json
    └── .env.local
```

---

# 🔧 8. Setup & Installation

### **Prerequisites**

* Node.js 18+
* Python 3.11+
* Git
* Google Cloud Console access
* YouTube Data API enabled

---

# 🔐 9. Google Cloud Setup (OAuth)

### Step 1 – Create Project

### Step 2 – Enable *YouTube Data API v3*

### Step 3 – Create OAuth Client ID

* User Type: **External**
* Scopes:

  * youtube.force-ssl
  * youtube.readonly
  * openid, email, profile

**Authorized Redirect URIs:**

Local:

```
http://localhost:8000/oauth/callback
```

Production:

```
https://youtube-ai-agent-backend.onrender.com/oauth/callback
```

### Step 4 – Create API Key

Restrict usage to **YouTube Data API**.

---

# 🖥️ 10. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
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

Start server:

```bash
uvicorn main:app --reload --port 8000
```

---

# 💻 11. Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local`:

```
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:8000/mcp
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3000
```

Run:

```bash
npm run dev
```

---

# 🌐 12. Deployment

## 12.1 Frontend — Vercel

Environment variables:

```
NEXT_PUBLIC_MCP_SERVER_URL=https://youtube-ai-agent-backend.onrender.com/mcp
NEXT_PUBLIC_BACKEND_URL=https://youtube-ai-agent-backend.onrender.com
NEXT_PUBLIC_FRONTEND_URL=https://youtube-ai-agent-two.vercel.app
```

Live:
**[https://youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)**

---

## 12.2 Backend — Render

Build:

```
pip install -r requirements.txt
```

Start:

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Live:
**[https://youtube-ai-agent-backend.onrender.com](https://youtube-ai-agent-backend.onrender.com)**

---

# 🔌 13. API Endpoints

### **FastAPI Server**

| Endpoint          | Description      |
| ----------------- | ---------------- |
| `/`               | Health check     |
| `/mcp/tools`      | List MCP tools   |
| `/mcp/call`       | Execute MCP tool |
| `/oauth/login`    | Start OAuth      |
| `/oauth/callback` | Token exchange   |
| `/oauth/userinfo` | User profile     |
| `/oauth/logout`   | Logout           |

### **Next.js (Frontend)**

| Endpoint              | Description                      |
| --------------------- | -------------------------------- |
| `/api/chat`           | Intent detection + MCP execution |
| `/api/oauth/login`    | Redirect to backend              |
| `/api/oauth/callback` | OAuth callback                   |

---

# 🛠️ 14. MCP Tools (22 Tools)

### **Discovery**

* search_videos
* search_channels
* trending_videos

### **Details**

* video_details
* channel_details

### **Actions**

* like_video
* unlike_video
* dislike_video
* comment_on_video

### **Subscriptions**

* subscribe_channel
* unsubscribe_channel
* my_subscriptions

### **Playlists**

* create_playlist
* add_to_playlist
* remove_from_playlist
* playlist_videos
* my_playlists

### **User Data**

* watch_history
* liked_videos
* my_channel

---

# ▶️ 15. Usage Flow

1. User opens frontend
2. Clicks **Connect YouTube**
3. OAuth login
4. Types a natural-language prompt
5. Next.js detects intent
6. Sends MCP request to backend
7. FastAPI executes tool
8. Results are rendered in UI components

---

# ⚠️ 16. Limitations

* No DB persistence
* Tokens not refreshed automatically
* YouTube API rate limits apply
* Some edge-case queries have basic error fallback

---

# 🚀 17. Future Enhancements

* Redis session store
* Automatic token refresh
* Semantic search using embeddings
* Transcript-based recommendations
* Advanced playlist manager
* UI themes / personalization

---

# 👤 18. Credits

**Developer:** Sushma Srinivas
Tech: Next.js, FastAPI, MCP, YouTube API
Deployment: Vercel + Render

---

# 🔗 19. Important Links

* Frontend: [https://youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)
* Backend: [https://youtube-ai-agent-backend.onrender.com](https://youtube-ai-agent-backend.onrender.com)
* GitHub: [https://github.com/sushxx99/youtube-ai-agent](https://github.com/sushxx99/youtube-ai-agent)

---

Absolutely — and I understand *exactly* what you want now:

### ✔ The same beautifully formatted “User Guide section”

### ✔ BUT **accurately reflecting only the features that *actually work***

### ✔ NOT including playlists, watch history, liked videos, or subscriptions

### ✔ Because your real output shows those did NOT work and were treated as search

So here is the **corrected, polished, honest, professional “How to Use the Web App” section**, in the exact same style as you liked — but fully accurate.

---

# 🧪 20. How to Use the Web App (User Guide)

This section explains **exactly how users can interact with the deployed app**, how to connect their YouTube account, what they can type, and which actions will truly reflect on their **real YouTube account**.

---

## 🔗 20.1 Open the Web App

Visit the live deployment:

**[https://youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)**

You will see:

* A clean chat interface
* A **Connect YouTube** button
* A text box where you can type prompts

---

## 🔐 20.2 Connect Your YouTube Account (OAuth Login)

1. Click **Connect YouTube**
2. Google OAuth opens
3. Select your Google account
4. Approve permissions:

   * View your YouTube data
   * Manage likes/dislikes
   * Post comments
   * View your YouTube channel info

Once done:

✔ Your YouTube profile picture appears
✔ You are now **authenticated**
✔ Any supported action you perform will apply to your **actual YouTube account**

> Example: Liking a video through the agent **likes it on your real YouTube**.

---

## 💬 20.3 Try These Prompts (Features That Actually Work)

These are **confirmed working features**, based on your real app’s outputs:

---

### 🔍 **Search & Trending**

```
search python tutorials
search for kubernetes beginners
search the latest AI news videos
find tech channels
show trending videos
```

---

### 👍 **Likes, Dislikes, and Related Video Actions**

These update your real YouTube account **immediately**:

```
like eWRfhZUzrAc
unlike this video
dislike fWjsdhR3z3c
like this video
```

---

### 💬 **Comments**

Fully supported — and they show up on real YouTube:

```
comment "Amazing tutorial!" on fWjsdhR3z3c
comment "Great explanation!" on K5KVEU3a
```

---

### 🔔 **Channel Actions**

These work based on your logs:

```
subscribe to Indently
subscribe to Fireship
unsubscribe <channel_id>
```

---

### 📄 **Video Details**

```
get details of fWjsdhR3z3c
```

---

### ▶️ **Pagination**

Your system fully supports next-page queries:

```
more
next
show more results
```

---

## 🚫 20.4 Features Not Supported (Important for Users)

To keep the README honest and accurate:

Your live system **does NOT support** these features (even though backend tools exist):

### ❌ Playlist creation

### ❌ Add to playlist

### ❌ Remove from playlist

### ❌ “Show my playlists”

### ❌ “Show my liked videos”

### ❌ “Show my watch history”

### ❌ “Show my subscriptions”

Your agent treated all these as **search queries**:

```
🎬 Found 10 videos about "my watch history."
```

So these actions do **not** affect the user’s real YouTube account.

---

## 🛠 20.5 What Happens Behind the Scenes

Once logged in:

✔ OAuth tokens stored in secure HTTP-only cookies
✔ Next.js forwards them to the backend
✔ FastAPI executes the appropriate MCP tool
✔ YouTube Data API processes your request
✔ Results return to the chat interface

All **supported actions** (likes, comments, subscriptions) directly update your YouTube account.

---

## 📌 20.6 Notes for Users

* You stay logged in even after refreshing the page
* Logout button is available on the header
* Likes/comments made through the agent appear **instantly** on YouTube
* The app does not store your personal data

---

## ⭐ 20.7 Short Demo Flow (What a Real User Experiences)

1. Open the app
2. Click **Connect YouTube**
3. Approve permissions
4. Try:

   ```
   search python for beginners
   ```
5. You see 10 curated video results
6. Type:

   ```
   more
   ```
7. Try a real action:

   ```
   like eWRfhZUzrAc
   ```

   → This action reflects on your **actual YouTube account**
8. Comment:

   ```
   comment "Amazing tutorial!" on fWjsdhR3z3c
   ```

   → Comment appears on YouTube
9. Subscribe:

   ```
   subscribe to Indently
   ```

Everything above is **verified working** and based on your real outputs.

---





