"""
Database Connection Manager
============================
Enterprise-grade database connection management with support for:
- PostgreSQL
- MySQL/MariaDB
- SQLite
- Connection pooling
- Health checks
- Automatic reconnection
"""

import logging
from contextlib import contextmanager
from typing import Optional, Dict, Any, Generator
from sqlalchemy import create_engine, Engine, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import QueuePool, NullPool
from sqlalchemy.exc import OperationalError, DisconnectionError
import time
from urllib.parse import urlparse

from config import Config

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Production-ready database connection manager with:
    - Multi-database support
    - Connection pooling
    - Health monitoring
    - Automatic reconnection
    - Transaction management
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            database_url: Database connection URL. If None, uses Config.DATABASE_URL
        """
        self.database_url = database_url or Config.DATABASE_URL
        self.engine: Optional[Engine] = None
        self.SessionLocal: Optional[sessionmaker] = None
        self._connection_pool_size = 20
        self._max_overflow = 10
        self._pool_timeout = 30
        self._pool_recycle = 3600
        self._last_health_check = 0
        self._health_check_interval = 60
        
        self._initialize_engine()
    
    def _initialize_engine(self) -> None:
        """Initialize SQLAlchemy engine with appropriate configuration."""
        try:
            parsed_url = urlparse(self.database_url)
            db_type = parsed_url.scheme.split('+')[0] if '+' in parsed_url.scheme else parsed_url.scheme
            
            # Configure engine based on database type
            engine_kwargs = self._get_engine_config(db_type)
            
            self.engine = create_engine(
                self.database_url,
                **engine_kwargs,
                echo=Config.DEBUG,
                future=True
            )
            
            # Add connection event listeners
            self._setup_event_listeners()
            
            # Create session factory
            self.SessionLocal = scoped_session(
                sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self.engine
                )
            )
            
            logger.info(f"Database engine initialized: {db_type} at {parsed_url.hostname or 'local'}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}", exc_info=True)
            raise
    
    def _get_engine_config(self, db_type: str) -> Dict[str, Any]:
        """Get engine configuration based on database type."""
        base_config = {
            "pool_pre_ping": True,
            "pool_recycle": self._pool_recycle,
            "connect_args": {}
        }
        
        if db_type == "sqlite":
            return {
                **base_config,
                "poolclass": NullPool,  # SQLite doesn't support connection pooling
                "connect_args": {"check_same_thread": False}
            }
        
        elif db_type in ("postgresql", "postgres"):
            return {
                **base_config,
                "poolclass": QueuePool,
                "pool_size": self._connection_pool_size,
                "max_overflow": self._max_overflow,
                "pool_timeout": self._pool_timeout,
                "connect_args": {
                    "connect_timeout": 10,
                    "application_name": Config.APP_NAME
                }
            }
        
        elif db_type in ("mysql", "mariadb"):
            return {
                **base_config,
                "poolclass": QueuePool,
                "pool_size": self._connection_pool_size,
                "max_overflow": self._max_overflow,
                "pool_timeout": self._pool_timeout,
                "connect_args": {
                    "connect_timeout": 10,
                    "charset": "utf8mb4"
                }
            }
        
        else:
            # Default configuration
            return {
                **base_config,
                "poolclass": QueuePool,
                "pool_size": self._connection_pool_size,
                "max_overflow": self._max_overflow
            }
    
    def _setup_event_listeners(self) -> None:
        """Setup SQLAlchemy event listeners for connection management."""
        
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            """Set SQLite pragmas for better performance."""
            if "sqlite" in self.database_url:
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.close()
        
        @event.listens_for(self.engine, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            """Log connection checkout."""
            if Config.DEBUG:
                logger.debug("Connection checked out from pool")
        
        @event.listens_for(self.engine, "checkin")
        def receive_checkin(dbapi_conn, connection_record):
            """Log connection checkin."""
            if Config.DEBUG:
                logger.debug("Connection returned to pool")
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session with automatic cleanup.
        
        Usage:
            with db_manager.get_session() as session:
                # Use session
                pass
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            session.close()
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform database health check.
        
        Returns:
            Dictionary with health status and metrics
        """
        current_time = time.time()
        
        # Throttle health checks
        if current_time - self._last_health_check < self._health_check_interval:
            return {
                "status": "healthy",
                "cached": True,
                "timestamp": current_time
            }
        
        try:
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            
            pool = self.engine.pool
            health_status = {
                "status": "healthy",
                "database_url": self._mask_database_url(),
                "pool_size": getattr(pool, "size", None),
                "checked_in": getattr(pool, "checkedin", None),
                "checked_out": getattr(pool, "checkedout", None),
                "overflow": getattr(pool, "overflow", None),
                "timestamp": current_time,
                "cached": False
            }
            
            self._last_health_check = current_time
            return health_status
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": current_time,
                "cached": False
            }
    
    def _mask_database_url(self) -> str:
        """Mask sensitive information in database URL."""
        parsed = urlparse(self.database_url)
        if parsed.password:
            masked_url = self.database_url.replace(
                f":{parsed.password}@",
                ":****@"
            )
            return masked_url
        return self.database_url
    
    def create_tables(self) -> None:
        """Create all database tables."""
        try:
            from database.models import Base
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}", exc_info=True)
            raise
    
    def drop_tables(self) -> None:
        """Drop all database tables (use with caution!)."""
        try:
            from database.models import Base
            Base.metadata.drop_all(bind=self.engine)
            logger.warning("All database tables dropped")
        except Exception as e:
            logger.error(f"Failed to drop tables: {e}", exc_info=True)
            raise
    
    def close(self) -> None:
        """Close all database connections."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_database_manager() -> DatabaseManager:
    """Get or create global database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def get_db_session() -> Generator[Session, None, None]:
    """
    Get database session (convenience function).
    
    Usage:
        for session in get_db_session():
            # Use session
            pass
    """
    db_manager = get_database_manager()
    yield from db_manager.get_session()

