"""
Legacy main.py - now imports the new refactored application.

This file maintains backward compatibility while delegating to the new architecture.
For production, use: uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

# Import the new refactored app
from app.main import app

# Re-export for backward compatibility
__all__ = ["app"]
