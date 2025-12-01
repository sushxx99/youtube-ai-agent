# YouTube AI Agent

> An intelligent conversational assistant that enables natural language interaction with YouTube through the Model Context Protocol (MCP)

<img width="1362" height="719" alt="image" src="https://github.com/user-attachments/assets/3769775a-e2ce-48d7-ae0c-39a87ed6b409" />

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://youtube-ai-agent-two.vercel.app)
[![Backend](https://img.shields.io/badge/backend-FastAPI-009688)](https://youtube-ai-agent-backend.onrender.com)
[![Frontend](https://img.shields.io/badge/frontend-Next.js%2014-000000)](https://youtube-ai-agent-two.vercel.app)

---

## Overview

YouTube AI Agent is a production-ready, full-stack application that brings conversational AI to YouTube. Users can search videos, like content, post comments, subscribe to channels, and more—all through natural language commands.

Built with modern technologies and deployed on enterprise-grade platforms, this project demonstrates advanced integration patterns between AI agents and external platforms using the Model Context Protocol.

**Live Application:** [youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)

---

## Table of Contents

- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [User Guide](#user-guide)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Key Features

### 🎯 Core Capabilities

- **Natural Language Interface** - Interact with YouTube using conversational commands
- **Intelligent Search** - Find videos, channels, and trending content
- **Real YouTube Actions** - Like videos, post comments, and subscribe to channels
- **OAuth Authentication** - Secure Google login with proper token management
- **Context Awareness** - Multi-turn conversations with memory
- **Pagination Support** - Browse through results seamlessly

### ✅ Verified Working Features

**Discovery & Search**
- Video search with advanced filters
- Channel discovery
- Trending content exploration
- Video details retrieval

**Authenticated Actions**
- Like/unlike videos
- Dislike videos
- Post comments
- Subscribe/unsubscribe from channels

**Enhanced Experience**
- Pagination through results
- Contextual recommendations
- Real-time feedback
- Responsive design

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│              (youtube-ai-agent-two.vercel.app)              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS + Secure Cookies
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Next.js Frontend (Vercel)                  │
├─────────────────────────────────────────────────────────────┤
│  • React-based UI Components                                │
│  • Intent Classification Engine                             │
│  • Session & Context Management                             │
│  • API Routes (/api/chat, /api/oauth/*)                     │
└────────────────────────┬────────────────────────────────────┘
                         │ POST /mcp/call
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                FastAPI MCP Server (Render)                   │
├─────────────────────────────────────────────────────────────┤
│  • MCP Tool Registry & Execution Engine                     │
│  • YouTube Data API v3 Client                               │
│  • OAuth 2.0 Flow Handler                                   │
│  • Async Request Processing                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Google OAuth 2.0    │
              │  YouTube Data API v3 │
              └──────────────────────┘
```

### Design Principles

- **Separation of Concerns** - Frontend handles UX, backend manages API interactions
- **Security First** - HTTP-only cookies, CORS policies, OAuth best practices
- **Scalability** - Async operations, efficient state management
- **Extensibility** - Modular MCP tool system for easy feature additions

---

## Technology Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** JavaScript/React
- **Styling:** CSS Modules
- **Deployment:** Vercel

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **HTTP Client:** httpx
- **Server:** Uvicorn
- **Deployment:** Render

### External Services
- **Authentication:** Google OAuth 2.0
- **Platform API:** YouTube Data API v3
- **Protocol:** Model Context Protocol (MCP)

---

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Google Cloud Console account
- Git

### Google Cloud Setup

1. **Create a Google Cloud Project**
   - Visit [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project

2. **Enable YouTube Data API v3**
   - Navigate to APIs & Services → Library
   - Search for "YouTube Data API v3"
   - Click Enable

3. **Configure OAuth 2.0**
   - Go to APIs & Services → Credentials
   - Create OAuth 2.0 Client ID
   - Application type: Web application
   - Authorized redirect URIs:
     - Development: `http://localhost:8000/oauth/callback`
     - Production: `https://youtube-ai-agent-backend.onrender.com/oauth/callback`

4. **Set OAuth Scopes**
   - `https://www.googleapis.com/auth/youtube.force-ssl`
   - `https://www.googleapis.com/auth/youtube.readonly`
   - `openid`, `email`, `profile`

5. **Create API Key**
   - Create credentials → API Key
   - Restrict to YouTube Data API v3

### Backend Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/oauth/callback
YOUTUBE_API_KEY=your_api_key_here
FRONTEND_URL=http://localhost:3000
EOF

# Start server
uvicorn main:app --reload --port 8000
```

Server will be available at `http://localhost:8000`

### Frontend Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:8000/mcp
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3000
EOF

# Start development server
npm run dev
```

Application will be available at `http://localhost:3000`

---

## User Guide

### Getting Started

1. **Access the Application**
   
   Visit [youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)

2. **Connect Your YouTube Account**
   
   - Click the "Connect YouTube" button
   - Sign in with your Google account
   - Authorize the requested permissions
   - Your profile picture appears when connected

3. **Start Conversing**
   
   Type natural language commands in the chat interface

### Example Commands

#### Search & Discovery

```
search python tutorials
find videos about machine learning
show trending videos
search tech channels
get details of [video_id]
```

#### Video Interactions

```
like [video_id]
unlike [video_id]
dislike [video_id]
comment "Great video!" on [video_id]
```

#### Channel Management

```
subscribe to [channel_name]
unsubscribe from [channel_id]
```

#### Navigation

```
more
next
show more results
```

### Important Notes

**Supported Features:**
- Video and channel search
- Trending videos
- Like/unlike/dislike actions
- Commenting on videos
- Channel subscriptions
- Video details
- Result pagination

**Current Limitations:**
- Playlist management not yet implemented
- Watch history retrieval unavailable
- Liked videos list unavailable
- Subscription list unavailable

All supported actions directly affect your real YouTube account in real-time.

---

## API Reference

### Backend Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/mcp/tools` | GET | List available MCP tools |
| `/mcp/call` | POST | Execute MCP tool |
| `/oauth/login` | GET | Initiate OAuth flow |
| `/oauth/callback` | GET | OAuth callback handler |
| `/oauth/userinfo` | GET | Get authenticated user info |
| `/oauth/logout` | POST | Logout user |

### Frontend API Routes

| Route | Description |
|-------|-------------|
| `/api/chat` | Process chat messages and execute tools |
| `/api/oauth/login` | Redirect to backend OAuth |
| `/api/oauth/callback` | Handle OAuth callback |

### MCP Tools

#### Discovery Tools
- `search_videos` - Search for videos by query
- `search_channels` - Find channels
- `trending_videos` - Get trending content

#### Detail Tools
- `video_details` - Retrieve video information
- `channel_details` - Get channel information

#### Action Tools
- `like_video` - Like a video
- `unlike_video` - Remove like from video
- `dislike_video` - Dislike a video
- `comment_on_video` - Post a comment

#### Subscription Tools
- `subscribe_channel` - Subscribe to a channel
- `unsubscribe_channel` - Unsubscribe from a channel

---

## Deployment

### Frontend (Vercel)

1. **Connect Repository**
   - Import your GitHub repository to Vercel

2. **Configure Environment Variables**
   ```
   NEXT_PUBLIC_MCP_SERVER_URL=https://youtube-ai-agent-backend.onrender.com/mcp
   NEXT_PUBLIC_BACKEND_URL=https://youtube-ai-agent-backend.onrender.com
   NEXT_PUBLIC_FRONTEND_URL=https://youtube-ai-agent-two.vercel.app
   ```

3. **Deploy**
   - Vercel auto-deploys on push to main branch

### Backend (Render)

1. **Create Web Service**
   - Connect your GitHub repository

2. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REDIRECT_URI=https://youtube-ai-agent-backend.onrender.com/oauth/callback
   YOUTUBE_API_KEY=your_api_key
   FRONTEND_URL=https://youtube-ai-agent-two.vercel.app
   ```

4. **Deploy**
   - Render auto-deploys on push to main branch

---

## Project Structure

```
youtube-ai-agent/
│
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── mcp_server.py          # MCP tool registry and executor
│   ├── oauth.py               # OAuth 2.0 implementation
│   ├── youtube_tools.py       # YouTube API client and tools
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables (gitignored)
│
└── frontend/
    ├── app/
    │   ├── page.js            # Main chat interface
    │   ├── layout.js          # Root layout component
    │   ├── globals.css        # Global styles
    │   ├── api/
    │   │   └── chat/
    │   │       └── route.js   # Chat API endpoint
    │   └── oauth/
    │       ├── login/
    │       │   └── route.js   # OAuth login route
    │       └── callback/
    │           └── route.js   # OAuth callback route
    │
    ├── components/
    │   ├── MessageBubble.jsx  # Chat message component
    │   ├── VideoCard.jsx      # Video display component
    │   └── Loader.jsx         # Loading indicator
    │
    ├── package.json           # Node dependencies
    ├── next.config.js         # Next.js configuration
    └── .env.local             # Environment variables (gitignored)
```

---

## Future Enhancements

- **Session Persistence** - Redis-backed session storage
- **Token Refresh** - Automatic OAuth token renewal
- **Advanced Search** - Semantic search using embeddings
- **Playlist Management** - Full CRUD operations
- **User Preferences** - Customizable interface and behavior
- **Analytics Dashboard** - Usage statistics and insights
- **Multi-language Support** - Internationalization
- **Voice Commands** - Speech-to-text integration

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Credits

**Developer:** Sushma Srinivas

**Technologies:** Next.js, FastAPI, Model Context Protocol, YouTube Data API v3

**Deployment:** Vercel (Frontend) + Render (Backend)

---

## Links

- **Live Application:** [youtube-ai-agent-two.vercel.app](https://youtube-ai-agent-two.vercel.app)
- **Backend API:** [youtube-ai-agent-backend.onrender.com](https://youtube-ai-agent-backend.onrender.com)
- **GitHub Repository:** [github.com/sushxx99/youtube-ai-agent](https://github.com/sushxx99/youtube-ai-agent)

---
