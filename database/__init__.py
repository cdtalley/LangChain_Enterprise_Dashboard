"""
Database Abstraction Layer
==========================
Production-ready database connectivity supporting multiple database backends.
"""

from .connection_manager import DatabaseManager, get_db_session
from .models import Base

__all__ = ["DatabaseManager", "get_db_session", "Base"]

