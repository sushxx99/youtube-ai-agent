import traceback
import logging
from typing import Dict, Any, Optional
from fastapi import Request
from youtube_tools import yt, YouTubeAPIError

logger = logging.getLogger(__name__)

# ============================================================
# HELPER: EXTRACT TOKEN FROM REQUEST
# ============================================================

def get_auth_token(request: Request) -> Optional[str]:
    """
    Extract auth token from:
    1. Authorization header (from frontend localStorage)
    2. Cookies
    3. Raw Cookie header
    """

    # 1️⃣ NEW — Authorization header
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "", 1).strip()
        if token:
            return token

    # 2️⃣ Cookies (Render → Vercel)
    token = request.cookies.get("yt_access_token")
    if token:
        return token

    # 3️⃣ Raw Cookie header
    cookie_header = request.headers.get("cookie", "")
    if cookie_header:
        for cookie in cookie_header.split(";"):
            cookie = cookie.strip()
            if cookie.startswith("yt_access_token="):
                return cookie.split("=", 1)[1]

    return None

# ============================================================
# MCP TOOL SCHEMAS (unchanged)
# ============================================================

MCP_TOOLS_SCHEMA = [
    {
        "name": "search_videos",
        "description": "Search for YouTube videos. Returns video results with snippets, statistics, and metadata. Use this for finding videos on any topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g., 'python tutorials', 'cooking recipes')"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Number of results to return (1-50)",
                    "default": 10
                },
                "page_token": {
                    "type": "string",
                    "description": "Token for pagination (get from previous response nextPageToken)"
                },
                "order": {
                    "type": "string",
                    "enum": ["relevance", "date", "viewCount", "rating"],
                    "description": "How to order results",
                    "default": "relevance"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_channels",
        "description": "Search for YouTube channels. Returns channel information including subscriber count and description.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Channel search query"
                },
                "max_results": {
                    "type": "integer",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "trending_videos",
        "description": "Get currently trending videos. Returns popular videos by region.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category_id": {
                    "type": "string",
                    "description": "Category ID (e.g., '10' for Music, '20' for Gaming)"
                },
                "region_code": {
                    "type": "string",
                    "description": "Two-letter country code (e.g., 'US', 'GB', 'IN')",
                    "default": "US"
                },
                "max_results": {
                    "type": "integer",
                    "default": 25
                }
            }
        }
    },
    {
        "name": "video_details",
        "description": "Get detailed information about specific video(s). Includes statistics, description, tags, and metadata.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_id": {
                    "type": "string",
                    "description": "Video ID or comma-separated list of video IDs"
                }
            },
            "required": ["video_id"]
        }
    },
    {
        "name": "video_comments",
        "description": "Get comments from a video. Returns top-level comments with metadata.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_id": {
                    "type": "string",
                    "description": "Video ID"
                },
                "max_results": {
                    "type": "integer",
                    "default": 20
                },
                "order": {
                    "type": "string",
                    "enum": ["relevance", "time"],
                    "default": "relevance"
                }
            },
            "required": ["video_id"]
        }
    },
    {
        "name": "channel_details",
        "description": "Get detailed information about a channel including statistics and branding.",
        "input_schema": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "Channel ID"
                }
            },
            "required": ["channel_id"]
        }
    },
    {
        "name": "channel_videos",
        "description": "Get videos from a specific channel. Returns recent or popular uploads.",
        "input_schema": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "Channel ID"
                },
                "max_results": {
                    "type": "integer",
                    "default": 10
                },
                "order": {
                    "type": "string",
                    "enum": ["date", "viewCount", "rating"],
                    "default": "date"
                }
            },
            "required": ["channel_id"]
        }
    },
    {
        "name": "like_video",
        "description": "Like a video. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_id": {
                    "type": "string",
                    "description": "Video ID to like"
                }
            },
            "required": ["video_id"]
        }
    },
    {
        "name": "unlike_video",
        "description": "Remove like from a video. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_id": {
                    "type": "string",
                    "description": "Video ID to unlike"
                }
            },
            "required": ["video_id"]
        }
    },
    {
        "name": "dislike_video",
        "description": "Dislike a video. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_id": {
                    "type": "string",
                    "description": "Video ID to dislike"
                }
            },
            "required": ["video_id"]
        }
    },
    {
        "name": "comment_on_video",
        "description": "Post a comment on a video. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_id": {
                    "type": "string",
                    "description": "Video ID"
                },
                "text": {
                    "type": "string",
                    "description": "Comment text"
                }
            },
            "required": ["video_id", "text"]
        }
    },
    {
        "name": "subscribe_channel",
        "description": "Subscribe to a channel. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "channel_id": {
                    "type": "string",
                    "description": "Channel ID to subscribe to"
                }
            },
            "required": ["channel_id"]
        }
    },
    {
        "name": "unsubscribe_channel",
        "description": "Unsubscribe from a channel. Requires authentication and subscription ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "subscription_id": {
                    "type": "string",
                    "description": "Subscription ID (get from my_subscriptions)"
                }
            },
            "required": ["subscription_id"]
        }
    },
    {
        "name": "my_subscriptions",
        "description": "Get list of channels user is subscribed to. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "default": 50
                }
            }
        }
    },
    {
        "name": "create_playlist",
        "description": "Create a new playlist. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Playlist title"
                },
                "description": {
                    "type": "string",
                    "description": "Playlist description",
                    "default": ""
                },
                "privacy": {
                    "type": "string",
                    "enum": ["private", "public", "unlisted"],
                    "default": "private"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "add_to_playlist",
        "description": "Add a video to a playlist. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "playlist_id": {
                    "type": "string",
                    "description": "Playlist ID"
                },
                "video_id": {
                    "type": "string",
                    "description": "Video ID to add"
                }
            },
            "required": ["playlist_id", "video_id"]
        }
    },
    {
        "name": "remove_from_playlist",
        "description": "Remove a video from a playlist. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "playlist_item_id": {
                    "type": "string",
                    "description": "Playlist item ID (not video ID)"
                }
            },
            "required": ["playlist_item_id"]
        }
    },
    {
        "name": "my_playlists",
        "description": "Get user's playlists. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "default": 50
                }
            }
        }
    },
    {
        "name": "playlist_videos",
        "description": "Get videos in a specific playlist. Requires authentication for private playlists.",
        "input_schema": {
            "type": "object",
            "properties": {
                "playlist_id": {
                    "type": "string",
                    "description": "Playlist ID"
                },
                "max_results": {
                    "type": "integer",
                    "default": 50
                }
            },
            "required": ["playlist_id"]
        }
    },
    {
        "name": "my_channel",
        "description": "Get authenticated user's channel information. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "watch_history",
        "description": "Get user's watch history. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "default": 50
                }
            }
        }
    },
    {
        "name": "liked_videos",
        "description": "Get user's liked videos. Requires authentication.",
        "input_schema": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "default": 50
                }
            }
        }
    }
]


# ============================================================
# TOOL EXECUTION FUNCTIONS
# ============================================================

async def execute_tool(tool_name: str, arguments: Dict[str, Any], request: Request) -> Dict[str, Any]:
    """
    Main tool executor with comprehensive error handling and response formatting
    """
    
    # 🔥 FIX: Use helper function to get token
    token = get_auth_token(request)
    
    # Log token status for debugging
    if token:
        logger.info(f"Auth token found for {tool_name}")
    else:
        logger.warning(f"No auth token for {tool_name}")
    
    try:
        # Route to appropriate tool
        if tool_name == "search_videos":
            result = await yt.search_videos(
                query=arguments["query"],
                max_results=arguments.get("max_results", 10),
                page_token=arguments.get("page_token"),
                order=arguments.get("order", "relevance"),
                token=token
            )
            
        elif tool_name == "search_channels":
            result = await yt.search_channels(
                query=arguments["query"],
                max_results=arguments.get("max_results", 10)
            )
            
        elif tool_name == "trending_videos":
            result = await yt.trending_videos(
                category_id=arguments.get("category_id"),
                region_code=arguments.get("region_code", "US"),
                max_results=arguments.get("max_results", 25),
                token=token
            )
            
        elif tool_name == "video_details":
            result = await yt.video_details(arguments["video_id"], token)
            
        elif tool_name == "video_comments":
            result = await yt.video_comments(
                video_id=arguments["video_id"],
                max_results=arguments.get("max_results", 20),
                order=arguments.get("order", "relevance")
            )
            
        elif tool_name == "channel_details":
            result = await yt.channel_details(arguments["channel_id"])
            
        elif tool_name == "channel_videos":
            result = await yt.channel_videos(
                channel_id=arguments["channel_id"],
                max_results=arguments.get("max_results", 10),
                order=arguments.get("order", "date")
            )
            
        # Authenticated tools
        elif tool_name == "like_video":
            if not token:
                logger.error("like_video called without token")
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.like_video(token, arguments["video_id"])
            
        elif tool_name == "unlike_video":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.unlike_video(token, arguments["video_id"])
            
        elif tool_name == "dislike_video":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.dislike_video(token, arguments["video_id"])
            
        elif tool_name == "comment_on_video":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.comment(token, arguments["video_id"], arguments["text"])
            
        elif tool_name == "subscribe_channel":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.subscribe(token, arguments["channel_id"])
            
        elif tool_name == "unsubscribe_channel":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.unsubscribe(token, arguments["subscription_id"])
            
        elif tool_name == "my_subscriptions":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.my_subscriptions(token, arguments.get("max_results", 50))
            
        elif tool_name == "create_playlist":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.create_playlist(
                token,
                arguments["title"],
                arguments.get("description", ""),
                arguments.get("privacy", "private")
            )
            
        elif tool_name == "add_to_playlist":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.add_to_playlist(
                token,
                arguments["playlist_id"],
                arguments["video_id"]
            )
            
        elif tool_name == "remove_from_playlist":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.remove_from_playlist(token, arguments["playlist_item_id"])
            
        elif tool_name == "my_playlists":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.user_playlists(token, arguments.get("max_results", 50))
            
        elif tool_name == "playlist_videos":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.playlist_videos(
                token,
                arguments["playlist_id"],
                arguments.get("max_results", 50)
            )
            
        elif tool_name == "my_channel":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.my_channel(token)
            
        elif tool_name == "watch_history":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.watch_history(token, arguments.get("max_results", 50))
            
        elif tool_name == "liked_videos":
            if not token:
                return {
                    "success": False,
                    "error": "Authentication required",
                    "auth_required": True
                }
            result = await yt.liked_videos(token, arguments.get("max_results", 50))
            
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "available_tools": [t["name"] for t in MCP_TOOLS_SCHEMA]
            }
        
        # Return standardized response
        return {
            "success": True,
            "tool": tool_name,
            "data": result
        }
        
    except YouTubeAPIError as e:
        logger.error(f"YouTube API error in {tool_name}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "tool": tool_name
        }
        
    except Exception as e:
        logger.error(f"Unexpected error in {tool_name}: {str(e)}\n{traceback.format_exc()}")
        return {
            "success": False,
            "error": f"Internal error: {str(e)}",
            "tool": tool_name,
            "trace": traceback.format_exc()
        }