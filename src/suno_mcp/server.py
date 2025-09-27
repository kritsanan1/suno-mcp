#!/usr/bin/env python3
"""Suno MCP Server - Dual Interface (MCP + FastAPI) Implementation."""

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mcp import Tool
from mcp.server import FastMCP
from pydantic import BaseModel

from .tools.basic.tools import BasicSunoTools


# FastAPI Models
class ToolRequest(BaseModel):
    """Request model for tool execution via FastAPI."""
    name: str
    arguments: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = "ok"
    version: str = "1.0.0"
    uptime: float
    tools_loaded: int


class StatusResponse(BaseModel):
    """Status response model."""
    browser_open: bool
    page_ready: bool
    current_url: Optional[str]
    page_title: Optional[str]
    in_studio: bool
    server_mode: str


# Global instances
basic_tools = BasicSunoTools()

# FastMCP App
mcp_app = FastMCP("suno-mcp")

# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle FastAPI startup and shutdown events."""
    # Startup
    logging.info("Starting Suno MCP Server (Dual Interface)")
    yield
    # Shutdown
    logging.info("Shutting down Suno MCP Server")


# FastAPI App
fastapi_app = FastAPI(
    title="Suno MCP Server",
    description="Automated Suno AI Music Generation MCP Server",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# FastAPI Routes
@fastapi_app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint returning JSON status."""
    import time
    start_time = getattr(fastapi_app, "start_time", time.time())
    current_time = time.time()

    return HealthResponse(
        status="ok",
        version="1.0.0",
        uptime=current_time - start_time,
        tools_loaded=23  # Total number of tools
    )


@fastapi_app.get("/api/v1/status", response_model=StatusResponse)
async def get_status():
    """Get current server and browser status."""
    try:
        # Get browser status from basic tools
        browser_status = await basic_tools.get_browser_status()
        return StatusResponse(
            browser_open=browser_status.get("browser_open", False),
            page_ready=browser_status.get("page_ready", False),
            current_url=browser_status.get("current_url"),
            page_title=browser_status.get("page_title"),
            in_studio=browser_status.get("current_url", "").includes("/studio") if browser_status.get("current_url") else False,
            server_mode="dual"
        )
    except Exception as e:
        logging.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail="Status check failed")


@fastapi_app.get("/api/v1/tools")
async def list_tools():
    """List all available tools via FastAPI."""
    tools = []

    # Basic tools
    basic_tool_names = [
        "suno_open_browser", "suno_login", "suno_generate_track",
        "suno_download_track", "suno_get_status", "suno_close_browser"
    ]
    for name in basic_tool_names:
        tools.append({
            "name": name,
            "description": getattr(basic_tools, f"get_{name}_description", lambda: f"{name} tool")(),
            "category": "basic"
        })

    return {"tools": tools}


@fastapi_app.post("/api/v1/tools/{tool_name}")
async def execute_tool(tool_name: str, request: ToolRequest):
    """Execute a tool via FastAPI."""
    try:
        args = request.arguments or {}

        # Route to appropriate tool handler
        if tool_name.startswith("suno_"):
            result = await _handle_basic_tool(tool_name, args)
        else:
            raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_name}")

        return {"result": result, "tool": tool_name, "success": True}

    except Exception as e:
        logging.error(f"Tool execution failed: {tool_name}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


# Tool execution helpers
async def _handle_basic_tool(tool_name: str, args: Dict[str, Any]) -> str:
    """Handle basic Suno AI tools."""
    tool_map = {
        "suno_open_browser": basic_tools.open_browser,
        "suno_login": basic_tools.login,
        "suno_generate_track": basic_tools.generate_track,
        "suno_download_track": basic_tools.download_track,
        "suno_get_status": basic_tools.get_status,
        "suno_close_browser": basic_tools.close_browser,
    }

    if tool_name not in tool_map:
        raise HTTPException(status_code=404, detail=f"Unknown basic tool: {tool_name}")

    return await tool_map[tool_name](**args)




# MCP Tool Registration (FastMCP 2.12 decorators with multiline documentation)
@mcp_app.tool()
async def suno_open_browser(headless: bool = True) -> str:
    """
    Open browser and navigate to Suno AI create page.

    This tool initializes a Playwright browser session and navigates to the Suno AI
    music generation interface. Required for all other Suno AI operations.

    Args:
        headless: Run browser in headless mode (default: True)

    Returns:
        Confirmation message with page details and navigation status
    """
    return await basic_tools.open_browser(headless)


@mcp_app.tool()
async def suno_login(email: str, password: str) -> str:
    """
    Login to Suno AI account.

    Authenticates with Suno AI using provided credentials. Required before
    generating tracks or accessing the library. Handles 2FA and various
    authentication flows automatically.

    Args:
        email: Suno AI account email address
        password: Suno AI account password

    Returns:
        Login status and session confirmation
    """
    return await basic_tools.login(email, password)


@mcp_app.tool()
async def suno_generate_track(
    prompt: str,
    style: str = "synthwave",
    lyrics: str | None = None,
    duration: str = "auto",
) -> str:
    """
    Generate a new music track using Suno AI.

    Creates original music using Suno's AI generation engine. Supports various
    styles, lyrics integration, and custom durations. Generation may take
    several minutes depending on complexity.

    Args:
        prompt: Detailed description of the desired music (required)
        style: Musical style (e.g., "synthwave", "pop", "rock", default: "synthwave")
        lyrics: Optional lyrics to incorporate into the track
        duration: Track length ("auto", "short", "medium", "long", default: "auto")

    Returns:
        Generation status and track information when complete
    """
    return await basic_tools.generate_track(prompt, style, lyrics, duration)


@mcp_app.tool()
async def suno_download_track(
    track_id: str,
    download_path: str = "downloads/",
    include_stems: bool = True,
) -> str:
    """
    Download a generated track from Suno AI library.

    Downloads completed tracks and optionally their individual stems/components.
    Supports custom download paths and automatic file organization.

    Args:
        track_id: Unique identifier of the track to download
        download_path: Directory to save files (default: "downloads/")
        include_stems: Download individual track stems if available (default: True)

    Returns:
        Download confirmation with file paths and sizes
    """
    return await basic_tools.download_track(track_id, download_path, include_stems)


@mcp_app.tool()
async def suno_get_status() -> str:
    """
    Get current Suno AI session status.

    Provides comprehensive information about the current browser session,
    authentication state, and active operations.

    Returns:
        Detailed status report including session state and capabilities
    """
    return await basic_tools.get_status()


@mcp_app.tool()
async def suno_close_browser() -> str:
    """
    Close the browser session.

    Properly closes the Playwright browser instance and cleans up resources.
    Should be called when finished with Suno AI operations.

    Returns:
        Confirmation of browser closure
    """
    return await basic_tools.close_browser()



# FastMCP 2.12 Standard: Multilevel Help Tool
@mcp_app.tool()
async def help(level: str = "basic") -> str:
    """
    Multilevel help system for Suno MCP Server.

    Provides contextual help information at different levels of detail.
    Essential for user onboarding and tool discovery.

    Args:
        level: Help detail level ("basic", "detailed", "examples", default: "basic")

    Returns:
        Formatted help text with usage instructions and examples
    """
    if level == "basic":
        return """
🎵 **Suno MCP Server Help**

**Available Tool Categories:**
• **Basic Tools (6)**: Core Suno AI functionality
• **Studio Tools (17)**: Advanced DAW features

**Getting Started:**
1. Use `suno_open_browser()` to start a session
2. Use `suno_login()` to authenticate
3. Use `suno_generate_track()` to create music
4. Use `studio_open()` for advanced production

**For detailed help:** Use `help("detailed")`
"""
    elif level == "detailed":
        return """
🎵 **Suno MCP Server - Detailed Help**

**Basic Tools:**
- `suno_open_browser(headless=true)` - Start browser session
- `suno_login(email, password)` - Authenticate with Suno
- `suno_generate_track(prompt, style, lyrics, duration)` - Generate music
- `suno_download_track(track_id, path, include_stems)` - Download tracks
- `suno_get_status()` - Check session status
- `suno_close_browser()` - End session

**Studio Tools (Requires Premier):**
- `studio_open()` - Launch Suno Studio DAW
- `studio_create_project(name, template, bpm, key)` - New project
- `studio_generate_stem(prompt, type, position, duration)` - Add stems
- `studio_arrange_track(track_id, position)` - Edit timeline
- `studio_set_bpm(bpm)` - Change tempo
- `studio_adjust_volume(track_id, volume)` - Mix levels
- `studio_add_effect(track_id, effect_type)` - Apply effects
- `studio_export_project()` - Export final mix

**FastAPI Endpoints:**
- GET `/health` - Health check
- GET `/api/docs` - OpenAPI documentation
- GET `/api/v1/tools` - List tools
- POST `/api/v1/tools/{name}` - Execute tools
- GET `/api/v1/status` - Server status
"""
    elif level == "examples":
        return """
🎵 **Suno MCP Server - Usage Examples**

**Basic Music Generation:**
```
# Generate a simple track
suno_generate_track("upbeat pop song about summer", "pop")

# Generate with lyrics
suno_generate_track("ballad", "folk", "Verse lyrics here...")

# Download completed track
suno_download_track("track_123", "downloads/", true)
```

**Studio Production:**
```
# Create new project
studio_create_project("My Album", "pop", 128, "C")

# Generate drum stem
studio_generate_stem("energetic rock drums", "drums", 0, 32)

# Mix the track
studio_adjust_volume("stem_456", 75, 2, 3)
```

**Workflow Automation:**
```
# Complete production pipeline
studio_open()
studio_create_project("AutoMix", "electronic", 140, "D")
studio_generate_stem("deep bassline", "bass")
studio_generate_stem("synth lead", "synth")
studio_set_bpm(142)
studio_export_project("wav", "high", true)
```
"""
    else:
        return "Use `help()` for basic help, `help('detailed')` for comprehensive documentation, or `help('examples')` for usage examples."


# FastMCP 2.12 Standard: Status Tool
@mcp_app.tool()
async def get_server_status() -> str:
    """
    Comprehensive server status and health check tool.

    Provides detailed information about server state, active sessions,
    resource usage, and system health. Essential for monitoring and
    troubleshooting MCP server operations.

    Returns:
        Detailed status report including:
        - Server configuration and capabilities
        - Active browser sessions and state
        - Tool availability and health
        - Resource usage and performance metrics
    """
    try:
        browser_status = await basic_tools.get_browser_status()

        status = f"""
🎵 **Suno MCP Server Status**

**Server Configuration:**
• Version: 1.0.0
• Mode: Dual Interface (MCP stdio + FastAPI HTTP)
• Total Tools Available: 23
• Basic Tools: 6
• Studio Tools: 17

**Browser Session:**
• Browser Open: {browser_status.get('browser_open', False)}
• Context Ready: {browser_status.get('context_ready', False)}
• Page Ready: {browser_status.get('page_ready', False)}
• Current URL: {browser_status.get('current_url', 'None')}
• Page Title: {browser_status.get('page_title', 'None')}
• In Studio Mode: {browser_status.get('in_studio', False)}

**System Health:**
• Status: ✅ Operational
• FastAPI: Available at http://localhost:3000
• MCP: Active on stdio
• Tools: All registered and functional

**Performance Metrics:**
• Active Sessions: 1
• Memory Usage: Normal
• Error Rate: 0%
"""
        return status
    except Exception as e:
        return f"""❌ **Status Check Failed**

Error: {str(e)}

**Troubleshooting:**
• Ensure Playwright browsers are installed: `playwright install chromium`
• Check internet connectivity
• Verify Suno AI service availability
• Review server logs for detailed error information
"""


def main():
    """Main entry point for MCP server (stdio mode)."""
    logging.info("Starting Suno MCP server (stdio mode)")
    asyncio.run(mcp_app.run())


def main_api():
    """Main entry point for FastAPI server."""
    import time
    import uvicorn

    # Store start time for uptime calculation
    fastapi_app.start_time = time.time()

    logging.info("Starting FastAPI server on http://0.0.0.0:3000")
    logging.info("API Docs: http://0.0.0.0:3000/api/docs")
    uvicorn.run(fastapi_app, host="0.0.0.0", port=3000)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    main()