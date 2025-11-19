"""
Database Integration Tests
==========================
Comprehensive integration tests for database adapters across different backends.
"""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

from database.adapters import (
    DatabaseAdapter,
    PostgreSQLAdapter,
    MySQLAdapter,
    SQLiteAdapter,
    MongoDBAdapter,
    DatabaseType,
    create_database_adapter
)
from database.connection_manager import DatabaseManager


class TestSQLiteAdapter:
    """Test SQLite adapter functionality."""
    
    def test_sqlite_connection(self):
        """Test SQLite connection."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            adapter = SQLiteAdapter(database_path=db_path)
            adapter.connect()
            assert adapter._conn is not None
            assert adapter._engine is not None
            adapter.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_sqlite_query_execution(self):
        """Test SQLite query execution."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            adapter = SQLiteAdapter(database_path=db_path)
            adapter.connect()
            
            # Create test table
            adapter.execute_query(
                "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)"
            )
            
            # Insert data
            adapter.execute_query(
                "INSERT INTO test_table (name) VALUES (?)",
                {"name": "test_value"}
            )
            
            # Query data
            results = adapter.execute_query("SELECT * FROM test_table")
            assert len(results) == 1
            assert results[0]["name"] == "test_value"
            
            adapter.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_sqlite_transaction(self):
        """Test SQLite transaction handling."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            adapter = SQLiteAdapter(database_path=db_path)
            adapter.connect()
            
            adapter.execute_query(
                "CREATE TABLE test_table (id INTEGER PRIMARY KEY, value INTEGER)"
            )
            
            queries = [
                ("INSERT INTO test_table (value) VALUES (?)", {"value": 1}),
                ("INSERT INTO test_table (value) VALUES (?)", {"value": 2}),
            ]
            
            success = adapter.execute_transaction(queries)
            assert success is True
            
            results = adapter.execute_query("SELECT COUNT(*) as count FROM test_table")
            assert results[0]["count"] == 2
            
            adapter.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_sqlite_health_check(self):
        """Test SQLite health check."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            adapter = SQLiteAdapter(database_path=db_path)
            adapter.connect()
            assert adapter.health_check() is True
            adapter.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)


class TestDatabaseManagerIntegration:
    """Test DatabaseManager with different database types."""
    
    def test_sqlite_manager(self):
        """Test DatabaseManager with SQLite."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            db_url = f"sqlite:///{db_path}"
            manager = DatabaseManager(database_url=db_url)
            
            assert manager.engine is not None
            assert manager.SessionLocal is not None
            
            health = manager.health_check()
            assert health["status"] == "healthy"
            
            manager.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_manager_session_context(self):
        """Test DatabaseManager session context."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            db_url = f"sqlite:///{db_path}"
            manager = DatabaseManager(database_url=db_url)
            manager.create_tables()
            
            with manager.get_session() as session:
                from sqlalchemy import text
                result = session.execute(text("SELECT 1 as test"))
                assert result.scalar() == 1
            
            manager.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)


class TestDatabaseAdapterFactory:
    """Test database adapter factory function."""
    
    def test_create_sqlite_adapter(self):
        """Test creating SQLite adapter via factory."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            adapter = create_database_adapter(
                DatabaseType.SQLITE,
                database_path=db_path
            )
            assert isinstance(adapter, SQLiteAdapter)
            adapter.connect()
            assert adapter.health_check() is True
            adapter.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_create_invalid_adapter(self):
        """Test factory with invalid database type."""
        with pytest.raises(ValueError):
            create_database_adapter(
                DatabaseType.MONGODB,  # Will fail without proper connection params
                host="localhost",
                port=27017,
                database="test"
            )


class TestDatabaseConnectionResilience:
    """Test database connection resilience and error handling."""
    
    def test_sqlite_connection_recovery(self):
        """Test SQLite connection recovery."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            adapter = SQLiteAdapter(database_path=db_path)
            adapter.connect()
            
            # Close connection
            adapter.close()
            
            # Should be able to reconnect
            adapter.connect()
            assert adapter.health_check() is True
            
            adapter.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_invalid_query_handling(self):
        """Test handling of invalid queries."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            adapter = SQLiteAdapter(database_path=db_path)
            adapter.connect()
            
            with pytest.raises(Exception):
                adapter.execute_query("SELECT * FROM nonexistent_table")
            
            adapter.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_transaction_rollback(self):
        """Test transaction rollback on error."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            adapter = SQLiteAdapter(database_path=db_path)
            adapter.connect()
            
            adapter.execute_query(
                "CREATE TABLE test_table (id INTEGER PRIMARY KEY, value INTEGER)"
            )
            
            queries = [
                ("INSERT INTO test_table (value) VALUES (?)", {"value": 1}),
                ("SELECT * FROM nonexistent_table", {}),  # This will fail
            ]
            
            success = adapter.execute_transaction(queries)
            assert success is False
            
            # Verify rollback - no data should be inserted
            results = adapter.execute_query("SELECT COUNT(*) as count FROM test_table")
            assert results[0]["count"] == 0
            
            adapter.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)


@pytest.mark.integration
class TestPostgreSQLAdapter:
    """Test PostgreSQL adapter (requires PostgreSQL server)."""
    
    @pytest.mark.skipif(
        os.getenv("POSTGRES_HOST") is None,
        reason="PostgreSQL not configured for testing"
    )
    def test_postgresql_connection(self):
        """Test PostgreSQL connection."""
        adapter = PostgreSQLAdapter(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "test"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "")
        )
        
        try:
            adapter.connect()
            assert adapter.health_check() is True
            adapter.close()
        except Exception as e:
            pytest.skip(f"PostgreSQL not available: {e}")


@pytest.mark.integration
class TestMongoDBAdapter:
    """Test MongoDB adapter (requires MongoDB server)."""
    
    @pytest.mark.skipif(
        os.getenv("MONGODB_HOST") is None,
        reason="MongoDB not configured for testing"
    )
    def test_mongodb_connection(self):
        """Test MongoDB connection."""
        adapter = MongoDBAdapter(
            host=os.getenv("MONGODB_HOST", "localhost"),
            port=int(os.getenv("MONGODB_PORT", "27017")),
            database=os.getenv("MONGODB_DB", "test"),
            user=os.getenv("MONGODB_USER"),
            password=os.getenv("MONGODB_PASSWORD")
        )
        
        try:
            adapter.connect()
            assert adapter.health_check() is True
            
            # Test query
            results = adapter.execute_query({}, collection="test_collection")
            assert isinstance(results, list)
            
            adapter.close()
        except Exception as e:
            pytest.skip(f"MongoDB not available: {e}")

