import os
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()
router = APIRouter()

# ENV VARIABLES
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI") 
FRONTEND_URL = os.getenv("FRONTEND_URL")


# REQUIRED SCOPES
# REQUIRED SCOPES
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.readonly"
]


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
@router.get("/oauth/login")
def oauth_login():
    # URL-encode scopes correctly
    scope_param = quote_plus(" ".join(SCOPES))

    url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&access_type=offline"
        f"&prompt=consent"
        f"&scope={scope_param}"
    )

    return RedirectResponse(url)


# ---------------------------------------------------------
# CALLBACK (Google → Backend)
# ---------------------------------------------------------
@router.get("/oauth/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return JSONResponse({"error": "No code returned"}, status_code=400)

    # Exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, data=data)
        tokens = token_res.json()

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    if not access_token:
        return JSONResponse(tokens, status_code=400)

    # Redirect to frontend
    response = RedirectResponse(f"{FRONTEND_URL}?connected=true")

# --------------------------
# SECURE CROSS-SITE COOKIES (REQUIRED FOR VERCEL → RENDER)
# --------------------------
    COOKIE_DOMAIN = "youtube-ai-agent-backend.onrender.com"

    cookie_params = {
        "httponly": True,
        "secure": True,           # required for SameSite=None
        "samesite": "None",       # required for cross-site cookies
        "path": "/",
        "domain": COOKIE_DOMAIN   # 🔥 CRITICAL FIX
    }

    # ACCESS TOKEN
    response.set_cookie(
        key="yt_access_token",
        value=access_token,
        max_age=3600,  # 1 hour
        **cookie_params
    )

    # REFRESH TOKEN (if provided by Google)
    if refresh_token:
        response.set_cookie(
            key="yt_refresh_token",
            value=refresh_token,
            max_age=60 * 60 * 24 * 30,  # 30 days
            **cookie_params
        )

    return response

# ---------------------------------------------------------
# USER INFO
# ---------------------------------------------------------
@router.get("/oauth/userinfo")
async def get_userinfo(request: Request):
    token = request.cookies.get("yt_access_token")

    if not token:
        return {"logged_in": False}

    # Use CORRECT Google OpenID endpoint
    url = "https://openidconnect.googleapis.com/v1/userinfo"

    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers={"Authorization": f"Bearer {token}"})

    if res.status_code != 200:
        return {"logged_in": False}

    profile = res.json()

    return {
        "logged_in": True,
        "profile": {
            "name": profile.get("name"),
            "email": profile.get("email"),
            "picture": profile.get("picture"),  # DO NOT MODIFY
        }
    }


# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
@router.get("/oauth/logout")
def logout():
    response = RedirectResponse(f"{FRONTEND_URL}/?logged_out=true")
    response.delete_cookie("yt_access_token", path="/")
    response.delete_cookie("yt_refresh_token", path="/")
    return response
