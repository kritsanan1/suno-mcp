"""Suno MCP Server - Automated Suno AI Music Generation.

This package provides an MCP (Model Context Protocol) server that automates
Suno AI music generation and Suno Studio DAW operations using Playwright.
"""

__version__ = "1.0.0"
__author__ = "Sandra Schipal"
__email__ = "sandra@example.com"

from .server import fastapi_app, mcp_app

__all__ = ["fastapi_app", "mcp_app"]