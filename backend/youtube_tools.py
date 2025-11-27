import os
import httpx
import logging
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3"


class YouTubeAPIError(Exception):
    """Custom exception for YouTube API errors"""
    pass


class YouTubeClient:
    """Professional YouTube API Client with comprehensive error handling"""
    
    def __init__(self):
        self.api_key = YOUTUBE_API_KEY  # Keep as fallback but won't use
        self.base_url = BASE_URL

    async def _safe_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Generic safe request handler with retries and error handling"""
        max_retries = 3
    
        for attempt in range(max_retries):
            try:
                url = f"{self.base_url}/{endpoint}"
            
                async with httpx.AsyncClient(timeout=15) as client:
                    if method.lower() == "get":
                        response = await client.get(url, **kwargs)
                    elif method.lower() == "post":
                        response = await client.post(url, **kwargs)
                    elif method.lower() == "delete":
                        response = await client.delete(url, **kwargs)
                    else:
                        raise ValueError(f"Unsupported HTTP method: {method}")

                # 🌟 FIX: Handle success with empty body (e.g., 204 No Content)
                    if response.status_code == 204 or not response.content:
                        return {"success": True}

                # Handle rate limiting
                    if response.status_code == 429:
                        logger.warning(f"Rate limited. Attempt {attempt + 1}/{max_retries}")
                        if attempt < max_retries - 1:
                            continue

                # Handle errors
                    if response.status_code >= 400:
                        error_data = response.json() if response.content else {}
                        error_msg = error_data.get("error", {}).get("message", "Unknown error")
                        raise YouTubeAPIError(
                            f"API Error {response.status_code}: {error_msg}"
                    )

                # Normal JSON response
                    return response.json()

            except httpx.TimeoutException:
                logger.error(f"Timeout on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    raise YouTubeAPIError("Request timeout after retries")

            except YouTubeAPIError:
                raise

            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Request failed: {str(e)}")
                    raise

        raise YouTubeAPIError("Max retries exceeded")


    async def public_get(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Public API call with API key"""
        params["key"] = self.api_key
        return await self._safe_request("get", endpoint, params=params)

    async def public_get_oauth(self, endpoint: str, params: Dict[str, Any], token: str) -> Dict[str, Any]:
        """Public API call using OAuth instead of API key"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        return await self._safe_request("get", endpoint, params=params, headers=headers)

    async def auth_request(
        self, 
        method: str, 
        endpoint: str, 
        token: str, 
        params: Optional[Dict] = None, 
        json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Authenticated API call with OAuth token"""
        if not token:
            raise YouTubeAPIError("Authentication token is required")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        kwargs = {"headers": headers}
        if params:
            kwargs["params"] = params
        if json:
            kwargs["json"] = json
        
        return await self._safe_request(method, endpoint, **kwargs)

    # ============================================================
    # SEARCH & DISCOVERY
    # ============================================================

    async def search_videos(
        self, 
        query: str, 
        max_results: int = 10,
        page_token: Optional[str] = None,
        order: str = "relevance",
        region_code: str = "US",
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search for videos with advanced filtering"""
        params = {
            "part": "snippet",
            "q": query,
            "maxResults": min(max_results, 50),
            "type": "video",
            "order": order,
            "regionCode": region_code,
            "relevanceLanguage": "en",
            "safeSearch": "moderate"
        }
        
        if page_token:
            params["pageToken"] = page_token
        
        # Use OAuth if token provided, otherwise use API key
        if token:
            result = await self.public_get_oauth("search", params, token)
        else:
            result = await self.public_get("search", params)
        
        # Enrich with video details
        if result.get("items"):
            video_ids = [item["id"]["videoId"] for item in result["items"]]
            details = await self.video_details(",".join(video_ids), token)
            
            details_map = {
                item["id"]: item for item in details.get("items", [])
            }
            
            for item in result["items"]:
                video_id = item["id"]["videoId"]
                if video_id in details_map:
                    item["statistics"] = details_map[video_id].get("statistics", {})
                    item["contentDetails"] = details_map[video_id].get("contentDetails", {})
        
        return result

    async def search_channels(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search for channels"""
        params = {
            "part": "snippet",
            "q": query,
            "maxResults": min(max_results, 50),
            "type": "channel",
            "order": "relevance"
        }
        return await self.public_get("search", params)

    async def trending_videos(
        self, 
        category_id: Optional[str] = None,
        region_code: str = "US",
        max_results: int = 25,
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get trending videos with optional category filter"""
        params = {
            "part": "snippet,statistics,contentDetails",
            "chart": "mostPopular",
            "regionCode": region_code,
            "maxResults": min(max_results, 50)
        }
        
        if category_id:
            params["videoCategoryId"] = category_id
        
        if token:
            return await self.public_get_oauth("videos", params, token)
        return await self.public_get("videos", params)

    # ============================================================
    # VIDEO OPERATIONS
    # ============================================================

    async def video_details(self, video_id: str, token: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed information about video(s)"""
        params = {
            "part": "snippet,statistics,contentDetails,status",
            "id": video_id
        }
        if token:
            return await self.public_get_oauth("videos", params, token)
        return await self.public_get("videos", params)

    async def video_comments(
        self, 
        video_id: str, 
        max_results: int = 20,
        order: str = "relevance"
    ) -> Dict[str, Any]:
        """Get comments for a video"""
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": min(max_results, 100),
            "order": order,
            "textFormat": "plainText"
        }
        return await self.public_get("commentThreads", params)

    # ============================================================
    # CHANNEL OPERATIONS
    # ============================================================

    async def channel_details(self, channel_id: str) -> Dict[str, Any]:
        """Get detailed channel information"""
        params = {
            "part": "snippet,statistics,contentDetails,brandingSettings",
            "id": channel_id
        }
        return await self.public_get("channels", params)

    async def channel_videos(
        self, 
        channel_id: str,
        max_results: int = 10,
        order: str = "date"
    ) -> Dict[str, Any]:
        """Get videos from a channel"""
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": min(max_results, 50),
            "order": order,
            "type": "video"
        }
        return await self.public_get("search", params)

    # ============================================================
    # USER ACTIONS (Authenticated)
    # ============================================================

    async def like_video(self, token: str, video_id: str) -> Dict[str, Any]:
        """Like a video"""
        params = {"id": video_id, "rating": "like"}
        result = await self.auth_request("post", "videos/rate", token, params=params)
        return {"success": True, "message": f"Successfully liked video {video_id}"}

    async def unlike_video(self, token: str, video_id: str) -> Dict[str, Any]:
        """Remove like from video"""
        params = {"id": video_id, "rating": "none"}
        result = await self.auth_request("post", "videos/rate", token, params=params)
        return {"success": True, "message": f"Successfully removed like from video {video_id}"}

    async def dislike_video(self, token: str, video_id: str) -> Dict[str, Any]:
        """Dislike a video"""
        params = {"id": video_id, "rating": "dislike"}
        result = await self.auth_request("post", "videos/rate", token, params=params)
        return {"success": True, "message": f"Successfully disliked video {video_id}"}

    async def comment(self, token: str, video_id: str, text: str) -> Dict[str, Any]:
        """Post a comment on a video"""
        body = {
            "snippet": {
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": text
                    }
                },
                "videoId": video_id
            }
        }
        
        params = {"part": "snippet"}
        result = await self.auth_request("post", "commentThreads", token, params=params, json=body)
        return {
            "success": True, 
            "message": f"Comment posted successfully",
            "comment_id": result.get("id")
        }

    async def subscribe(self, token: str, channel_id: str) -> Dict[str, Any]:
        """Subscribe to a channel"""
        body = {
            "snippet": {
                "resourceId": {
                    "kind": "youtube#channel",
                    "channelId": channel_id
                }
            }
        }
        
        params = {"part": "snippet"}
        result = await self.auth_request("post", "subscriptions", token, params=params, json=body)
        return {
            "success": True,
            "message": f"Successfully subscribed to channel",
            "subscription_id": result.get("id")
        }

    async def unsubscribe(self, token: str, subscription_id: str) -> Dict[str, Any]:
        """Unsubscribe from a channel"""
        params = {"id": subscription_id}
        await self.auth_request("delete", "subscriptions", token, params=params)
        return {"success": True, "message": "Successfully unsubscribed"}

    async def my_subscriptions(self, token: str, max_results: int = 50) -> Dict[str, Any]:
        """Get user's subscriptions"""
        params = {
            "part": "snippet,contentDetails",
            "mine": "true",
            "maxResults": min(max_results, 50)
        }
        return await self.auth_request("get", "subscriptions", token, params=params)

    # ============================================================
    # PLAYLIST OPERATIONS
    # ============================================================

    async def create_playlist(
        self, 
        token: str, 
        title: str, 
        description: str = "",
        privacy: str = "private"
    ) -> Dict[str, Any]:
        """Create a new playlist"""
        body = {
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": privacy  # private, public, unlisted
            }
        }
        
        params = {"part": "snippet,status"}
        result = await self.auth_request("post", "playlists", token, params=params, json=body)
        return {
            "success": True,
            "playlist_id": result.get("id"),
            "title": title
        }

    async def add_to_playlist(
        self, 
        token: str, 
        playlist_id: str, 
        video_id: str
    ) -> Dict[str, Any]:
        """Add video to playlist"""
        body = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
        
        params = {"part": "snippet"}
        result = await self.auth_request("post", "playlistItems", token, params=params, json=body)
        return {
            "success": True,
            "message": "Video added to playlist",
            "item_id": result.get("id")
        }

    async def remove_from_playlist(
        self, 
        token: str, 
        playlist_item_id: str
    ) -> Dict[str, Any]:
        """Remove video from playlist"""
        params = {"id": playlist_item_id}
        await self.auth_request("delete", "playlistItems", token, params=params)
        return {"success": True, "message": "Video removed from playlist"}

    async def user_playlists(self, token: str, max_results: int = 50) -> Dict[str, Any]:
        """Get user's playlists"""
        params = {
            "part": "snippet,contentDetails,status",
            "mine": "true",
            "maxResults": min(max_results, 50)
        }
        return await self.auth_request("get", "playlists", token, params=params)

    async def playlist_videos(
        self, 
        token: str, 
        playlist_id: str,
        max_results: int = 50
    ) -> Dict[str, Any]:
        """Get videos in a playlist"""
        params = {
            "part": "snippet,contentDetails,status",
            "playlistId": playlist_id,
            "maxResults": min(max_results, 50)
        }
        return await self.auth_request("get", "playlistItems", token, params=params)

    # ============================================================
    # USER DATA
    # ============================================================

    async def my_channel(self, token: str) -> Dict[str, Any]:
        """Get authenticated user's channel info"""
        params = {
            "part": "snippet,statistics,contentDetails",
            "mine": "true"
        }
        return await self.auth_request("get", "channels", token, params=params)

    async def watch_history(self, token: str, max_results: int = 50) -> Dict[str, Any]:
        """Get user's watch history"""
        params = {
            "part": "snippet,contentDetails",
            "mine": "true",
            "maxResults": min(max_results, 50)
        }
        return await self.auth_request("get", "activities", token, params=params)

    async def liked_videos(self, token: str, max_results: int = 50) -> Dict[str, Any]:
        """Get user's liked videos"""
        # First get the user's channel to find their likes playlist
        channel = await self.my_channel(token)
        
        if not channel.get("items"):
            return {"items": [], "message": "No channel found"}
        
        likes_playlist = channel["items"][0]["contentDetails"]["relatedPlaylists"].get("likes")
        
        if not likes_playlist:
            return {"items": [], "message": "Likes playlist not found"}
        
        return await self.playlist_videos(token, likes_playlist, max_results)


# ============================================================
# SINGLETON INSTANCE
# ============================================================

yt = YouTubeClient()