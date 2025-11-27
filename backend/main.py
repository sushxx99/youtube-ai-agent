from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mcp_server import execute_tool, MCP_TOOLS_SCHEMA
from oauth import router as oauth_router
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="YouTube MCP Server",
    description="Model Context Protocol server for YouTube API integration",
    version="1.0.0"
)

# ============================================================
# MIDDLEWARE
# ============================================================

# CORS Configuration 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",

        # Vercel production domain
        "https://youtube-ai-agent-two.vercel.app",

        # Vercel project domain
        "https://youtube-ai-agent.vercel.app",

        # Vercel preview domain
        "https://youtube-ai-agent-git-main-sushxx99s-projects.vercel.app",

        # 🔥 REQUIRED: Backend origin itself (Render)
        "https://youtube-ai-agent-backend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response
        logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
        
        # Add performance header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise

# ============================================================
# ROUTES
# ============================================================

# Include OAuth routes
app.include_router(oauth_router, tags=["OAuth"])

@app.get("/", tags=["Health"])
def home():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "YouTube MCP Server",
        "version": "1.0.0",
        "endpoints": {
            "oauth": "/oauth/login",
            "mcp_tools": "/mcp/tools",
            "mcp_call": "/mcp/call"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "youtube_api": "operational",
            "oauth": "operational",
            "mcp_server": "operational"
        }
    }

@app.get("/mcp/tools", tags=["MCP"])
def get_mcp_tools():
    """
    Get all available MCP tools with their schemas.
    This endpoint helps clients discover available tools.
    """
    return {
        "tools": MCP_TOOLS_SCHEMA,
        "total_count": len(MCP_TOOLS_SCHEMA)
    }

@app.post("/mcp/call", tags=["MCP"])
async def call_mcp_tool(request: Request):
    """
    Execute an MCP tool with given arguments.
    
    Request body:
    {
        "tool_name": "search_videos",
        "arguments": {
            "query": "python tutorials",
            "max_results": 10
        }
    }
    """
    try:
        body = await request.json()
        
        # Validate request
        if "tool_name" not in body:
            raise HTTPException(status_code=400, detail="Missing 'tool_name' in request")
        
        tool_name = body.get("tool_name")
        arguments = body.get("arguments", {})
        
        logger.info(f"Executing MCP tool: {tool_name} with args: {arguments}")
        
        # Execute tool
        result = await execute_tool(tool_name, arguments, request)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"MCP call error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Internal server error: {str(e)}"
            }
        )

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "path": str(request.url.path),
            "message": "The requested resource was not found"
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )

# ============================================================
# STARTUP/SHUTDOWN
# ============================================================

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 YouTube MCP Server starting up...")
    logger.info("✅ Server ready to accept requests")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 YouTube MCP Server shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )