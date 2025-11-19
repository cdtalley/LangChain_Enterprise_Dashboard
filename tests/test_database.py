"""
Database Tests
==============
Comprehensive tests for database connectivity and operations.
"""

import pytest
import os
import tempfile
from pathlib import Path
from sqlalchemy import text

from database.connection_manager import DatabaseManager
from database.models import Base, QueryLog, ModelRegistry


@pytest.fixture
def temp_db():
    """Create temporary SQLite database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    db_url = f"sqlite:///{path}"
    
    manager = DatabaseManager(database_url=db_url)
    manager.create_tables()
    
    yield manager
    
    manager.close()
    os.unlink(path)


@pytest.fixture
def db_session(temp_db):
    """Get database session for testing."""
    with temp_db.get_session() as session:
        yield session


class TestDatabaseManager:
    """Test database manager functionality."""
    
    def test_initialization(self, temp_db):
        """Test database manager initialization."""
        assert temp_db.engine is not None
        assert temp_db.SessionLocal is not None
    
    def test_health_check(self, temp_db):
        """Test database health check."""
        health = temp_db.health_check()
        assert health["status"] == "healthy"
        assert "timestamp" in health
    
    def test_session_context(self, temp_db):
        """Test session context manager."""
        with temp_db.get_session() as session:
            result = session.execute(text("SELECT 1"))
            assert result.scalar() == 1
    
    def test_connection_pooling(self, temp_db):
        """Test connection pooling."""
        health = temp_db.health_check()
        assert "pool_size" in health or health["status"] == "healthy"
    
    def test_create_tables(self, temp_db):
        """Test table creation."""
        # Tables should already be created by fixture
        with temp_db.get_session() as session:
            result = session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            )
            tables = [row[0] for row in result]
            assert "query_logs" in tables
            assert "model_registry" in tables


class TestDatabaseModels:
    """Test database models."""
    
    def test_query_log_creation(self, db_session):
        """Test creating query log entry."""
        log = QueryLog(
            query_text="Test query",
            response_text="Test response",
            execution_time_ms=100.5,
            model_used="test-model"
        )
        db_session.add(log)
        db_session.commit()
        
        assert log.id is not None
        assert log.created_at is not None
    
    def test_model_registry_creation(self, db_session):
        """Test creating model registry entry."""
        model = ModelRegistry(
            name="test-model",
            version="1.0.0",
            model_type="llm",
            stage="development",
            path="/path/to/model",
            description="Test model"
        )
        db_session.add(model)
        db_session.commit()
        
        assert model.id is not None
        assert model.is_active is True
    
    def test_model_registry_unique_name(self, db_session):
        """Test model registry unique name constraint."""
        model1 = ModelRegistry(
            name="unique-model",
            version="1.0.0",
            model_type="llm",
            path="/path/to/model"
        )
        db_session.add(model1)
        db_session.commit()
        
        model2 = ModelRegistry(
            name="unique-model",
            version="2.0.0",
            model_type="llm",
            path="/path/to/model2"
        )
        db_session.add(model2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()


class TestDatabaseOperations:
    """Test database operations."""
    
    def test_transaction_rollback(self, temp_db):
        """Test transaction rollback on error."""
        with temp_db.get_session() as session:
            log = QueryLog(
                query_text="Test",
                response_text="Test"
            )
            session.add(log)
            # Intentionally cause error
            session.execute(text("SELECT * FROM nonexistent_table"))
        
        # Session should have rolled back
        with temp_db.get_session() as session:
            count = session.query(QueryLog).count()
            assert count == 0
    
    def test_query_performance(self, db_session):
        """Test query performance."""
        import time
        
        # Create test data
        for i in range(10):
            log = QueryLog(
                query_text=f"Query {i}",
                response_text=f"Response {i}"
            )
            db_session.add(log)
        db_session.commit()
        
        # Measure query time
        start = time.time()
        logs = db_session.query(QueryLog).all()
        elapsed = time.time() - start
        
        assert len(logs) == 10
        assert elapsed < 1.0  # Should be fast

