from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
import os, httpx
from urllib.parse import urlencode

router = APIRouter()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")

SCOPES = [
    "openid",
    "profile",
    "email",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.readonly",
]


@router.get("/oauth/login")
def oauth_login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "scope": " ".join(SCOPES)
    }

    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    return RedirectResponse(url)


@router.get("/oauth/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "No code"}, status_code=400)

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

    response = RedirectResponse(f"{FRONTEND_URL}?connected=true")

    # COOKIE FIX — no domain!
    cookie_params = {
    "httponly": True,
    "secure": True,
    "samesite": "None",
    "path": "/"
}


    response.set_cookie("yt_access_token", access_token, max_age=3600, **cookie_params)

    if refresh_token:
        response.set_cookie(
            "yt_refresh_token",
            refresh_token,
            max_age=60 * 60 * 24 * 30,
            **cookie_params,
        )

    return response


@router.get("/oauth/userinfo")
async def userinfo(request: Request):
    token = request.cookies.get("yt_access_token")
    if not token:
        return {"logged_in": False}

    url = "https://openidconnect.googleapis.com/v1/userinfo"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers={"Authorization": f"Bearer {token}"})

    if r.status_code != 200:
        return {"logged_in": False}

    profile = r.json()

    return {
        "logged_in": True,
        "profile": {
            "name": profile.get("name"),
            "email": profile.get("email"),
            "picture": profile.get("picture"),
        },
    }


@router.get("/oauth/logout")
def logout():
    resp = RedirectResponse(f"{FRONTEND_URL}/?logout=true")
    resp.delete_cookie("yt_access_token", path="/")
    resp.delete_cookie("yt_refresh_token", path="/")
    return resp
