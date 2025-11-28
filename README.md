Perfect.
I will now generate your **complete README.md** in the **exact same style, layout, tone, spacing, emojis, and structure** as the sample — but using **your project’s content**.

Here is your **final GitHub-ready README**:

---

# 🎥 YouTube AI Agent – MCP-Powered Intelligent Assistant

A fully functional **Model Context Protocol (MCP)** powered YouTube assistant that integrates with the **YouTube Data API v3** through a custom **FastAPI backend** using **OAuth2**, with a modern, responsive **Next.js (React)** frontend deployed on **Vercel**.

This MCP Agent allows users to:

🔍 Search YouTube videos
📺 Fetch channel details & videos
🔥 View trending content
ℹ️ Fetch video metadata
❤️ Like / Unlike videos
💬 Comment on videos
🔔 Subscribe / Unsubscribe
🎵 Create & manage playlists
🕒 View watch history
📚 View liked videos
⚙️ Multi-turn natural language chat
🔐 Google OAuth2 login with secure cookies

---

# 🚀 Live Deployment

### **Frontend (Vercel)**

🔗 [https://youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)

### **Backend (Render)**

🔗 [https://youtube-ai-agent-backend.onrender.com](https://youtube-ai-agent-backend.onrender.com)

---

# 🏗 Project Architecture

```
youtube-ai-agent/
│
├── backend/                       # MCP Server (FastAPI)
│   ├── main.py                    # FastAPI app, routes, CORS
│   ├── mcp_server.py              # MCP tool dispatcher
│   ├── youtube_tools.py           # All 22 YouTube MCP tools
│   ├── oauth.py                   # Google OAuth2 login + callback
│   ├── requirements.txt           # Backend dependencies
│   └── .env                       # OAuth + API keys
│
├── frontend/                      # MCP Agent UI (Next.js 14)
│   ├── app/                       # App Router UI
│   ├── api/                       # Chat backend API (intent → MCP)
│   ├── components/                # Chat UI + Video Cards
│   ├── next.config.js
│   ├── package.json
│   └── .env.local
│
└── README.md                      # (This file)
```

---

# 🔐 OAuth2 Setup (Completed)

Backend uses:

✔ CLIENT_ID
✔ CLIENT_SECRET
✔ REDIRECT_URI
✔ Access Token
✔ Refresh Token (via Google login)

The backend securely stores tokens in **HTTP-only cookies**, allowing:

⚡ Automatic authentication
⚡ Protected MCP calls
⚡ No token exposure on frontend

---

# ⚙️ Backend Environment (Render)

Set these in Render Dashboard:

```
GOOGLE_CLIENT_ID=xxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxxx
GOOGLE_REDIRECT_URI=https://youtube-ai-agent-backend.onrender.com/oauth/callback
FRONTEND_URL=https://youtube-ai-agent-two.vercel.app
YOUTUBE_API_KEY=xxxxxxxxx
```

Backend auto-handles:

✔ OAuth login
✔ Token exchange
✔ Cookie storage
✔ MCP tool execution

---

# ⚙️ Frontend Environment (Vercel)

```
NEXT_PUBLIC_MCP_SERVER_URL=https://youtube-ai-agent-backend.onrender.com/mcp
NEXT_PUBLIC_BACKEND_URL=https://youtube-ai-agent-backend.onrender.com
NEXT_PUBLIC_FRONTEND_URL=https://youtube-ai-agent-two.vercel.app
```

---

# 🧠 MCP Tools Implemented

### **Discovery**

| MCP Tool        | Description           |
| --------------- | --------------------- |
| search_videos   | Search YouTube videos |
| search_channels | Search channels       |
| trending_videos | Fetch trending videos |

### **Details**

| MCP Tool        | Description    |
| --------------- | -------------- |
| video_details   | Video metadata |
| channel_details | Channel info   |
| video_comments  | Fetch comments |

### **Actions (OAuth)**

| MCP Tool         | Description      |
| ---------------- | ---------------- |
| like_video       | Like a video     |
| unlike_video     | Remove like      |
| dislike_video    | Dislike          |
| comment_on_video | Comment on video |

### **Subscriptions**

| MCP Tool            | Description             |
| ------------------- | ----------------------- |
| subscribe_channel   | Subscribe               |
| unsubscribe_channel | Unsubscribe             |
| my_subscriptions    | User subscriptions list |

### **Playlists**

| MCP Tool             | Description         |
| -------------------- | ------------------- |
| create_playlist      | Create playlist     |
| add_to_playlist      | Add video           |
| remove_from_playlist | Remove video        |
| my_playlists         | List user playlists |
| playlist_videos      | Playlist items      |

### **User Data**

| MCP Tool      | Description    |
| ------------- | -------------- |
| my_channel    | User’s channel |
| watch_history | History        |
| liked_videos  | Liked videos   |

---

# ⭐ New Features Added (Updated)

### ✅ 1. Fully Working Like / Unlike System

Works across:

✔ Search results
✔ Trending videos
✔ Channel videos
✔ User playlists
✔ User history
✔ User liked videos

Updates UI instantly.

---

### ✅ 2. Comment on Any Video

Example:

```
comment on dQw4w9WgXcQ "Amazing video!"
```

---

### ✅ 3. Playlist Management

Full create → add → remove workflow.

---

### ✅ 4. Multi-Turn Chat Context

The agent remembers:

* Your last search
* The previous list of videos
* What "like the first one" refers to

---

### ✅ 5. Trending with Region Support

```
show me trending videos
```

---

### 📱 Responsive UI

✔ Mobile-friendly
✔ Auto responsive grid
✔ Smooth transitions
✔ YouTube-style layout

---

# 🧩 System Flow

```
User
  ↓
Next.js Frontend (Chat UI + Video Grid)
  ↓ /api/chat
Intent Classifier (LLM)
  ↓ chooses MCP tool
Backend (FastAPI MCP Server)
  ↓
YouTube Data API v3
  ↓
Backend Response
  ↓
Frontend displays videos + actions
```

---

# 🛠 Local Development Guide

### **Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Runs at:
👉 [http://localhost:8000](http://localhost:8000)

---

### **Frontend**

```bash
cd frontend
npm install
npm run dev
```

Runs at:
👉 [http://localhost:3000](http://localhost:3000)

---

# 🧪 Example Commands

### 🔍 Search

```
python tutorials
travel vlogs
```

### 🎬 Channel Videos

```
channel tseries
```

### 🔥 Trending

```
trending videos
```

### ❤️ Like a Video

```
like dQw4w9WgXcQ
```

### 💬 Comment

```
comment on dQw4w9WgXcQ "Beautiful edit!"
```

### 🔔 Subscribe

```
subscribe to @mkbhd
```

### 📝 Playlist

```
create playlist coding
add dQw4w9WgXcQ to playlist coding
```

---

# 🎯 Assignment Requirements (Checked)

| Requirement                      | Status                |
| -------------------------------- | --------------------- |
| Build MCP Agent                  | ✅ Completed           |
| Integrate external API (YouTube) | ✅ Done                |
| Expose MCP tools                 | ✅ 22 tools            |
| Implement actions                | ❤️ 👍 💬 🔔           |
| Fully deployed                   | ✔ Vercel + Render     |
| Public GitHub Repo               | ✔ Yes                 |
| Good UI                          | ✔ Modern + Responsive |
| OAuth Integration                | ✔ Secure Cookies      |

---

# 🧑‍💻 Developer

**Sushma Srinivas**
MCP Agent Developer | FastAPI + Next.js | YouTube API Specialist

---

# 🎉 Built with ❤️ in 48 hours

Powered by **MCP + FastAPI + Next.js + YouTube Data API v3**
