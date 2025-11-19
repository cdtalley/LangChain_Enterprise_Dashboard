"""
Comprehensive Database Adapter Tests
====================================
Tests for all database adapters with proper mocking and error handling.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from database.adapters import (
    DatabaseType, DatabaseAdapter, PostgreSQLAdapter,
    MySQLAdapter, SQLiteAdapter, MongoDBAdapter, create_database_adapter
)


class TestPostgreSQLAdapter:
    """PostgreSQL adapter tests"""
    
    def test_init(self):
        adapter = PostgreSQLAdapter(
            host="localhost", port=5432, database="test",
            user="user", password="pass"
        )
        assert adapter.host == "localhost"
        assert adapter.port == 5432
        assert adapter.database == "test"
    
    @patch('database.adapters.create_engine')
    def test_connect_success(self, mock_engine):
        adapter = PostgreSQLAdapter(
            host="localhost", port=5432, database="test",
            user="user", password="pass"
        )
        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value = mock_conn
        
        result = adapter.connect()
        assert result == mock_conn
        mock_engine.assert_called_once()
    
    @patch('database.adapters.create_engine')
    def test_connect_failure(self, mock_engine):
        adapter = PostgreSQLAdapter(
            host="localhost", port=5432, database="test",
            user="user", password="pass"
        )
        mock_engine.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception):
            adapter.connect()
    
    def test_execute_query(self):
        adapter = PostgreSQLAdapter(
            host="localhost", port=5432, database="test",
            user="user", password="pass"
        )
        adapter._conn = MagicMock()
        adapter._conn.execute.return_value.keys.return_value = ["id", "name"]
        adapter._conn.execute.return_value.fetchall.return_value = [(1, "test")]
        
        result = adapter.execute_query("SELECT * FROM test")
        assert len(result) == 1
        assert result[0]["id"] == 1
    
    def test_health_check_success(self):
        adapter = PostgreSQLAdapter(
            host="localhost", port=5432, database="test",
            user="user", password="pass"
        )
        adapter.execute_query = Mock(return_value=[{"1": 1}])
        
        assert adapter.health_check() is True
    
    def test_health_check_failure(self):
        adapter = PostgreSQLAdapter(
            host="localhost", port=5432, database="test",
            user="user", password="pass"
        )
        adapter.execute_query = Mock(side_effect=Exception("DB error"))
        
        assert adapter.health_check() is False


class TestMySQLAdapter:
    """MySQL adapter tests"""
    
    def test_init(self):
        adapter = MySQLAdapter(
            host="localhost", port=3306, database="test",
            user="user", password="pass"
        )
        assert adapter.host == "localhost"
        assert adapter.port == 3306
    
    @patch('database.adapters.create_engine')
    def test_connect(self, mock_engine):
        adapter = MySQLAdapter(
            host="localhost", port=3306, database="test",
            user="user", password="pass"
        )
        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value = mock_conn
        
        result = adapter.connect()
        assert result == mock_conn


class TestSQLiteAdapter:
    """SQLite adapter tests"""
    
    def test_init(self):
        adapter = SQLiteAdapter(database_path=":memory:")
        assert adapter.database_path == ":memory:"
    
    def test_connect(self):
        adapter = SQLiteAdapter(database_path=":memory:")
        conn = adapter.connect()
        assert conn is not None
        adapter.close()
    
    def test_execute_query(self):
        adapter = SQLiteAdapter(database_path=":memory:")
        adapter.connect()
        
        adapter.execute_query("CREATE TABLE test (id INTEGER, name TEXT)")
        result = adapter.execute_query("INSERT INTO test VALUES (1, 'test')")
        rows = adapter.execute_query("SELECT * FROM test")
        
        assert len(rows) == 1
        adapter.close()


class TestMongoDBAdapter:
    """MongoDB adapter tests"""
    
    def test_init(self):
        adapter = MongoDBAdapter(
            host="localhost", port=27017, database="test"
        )
        assert adapter.host == "localhost"
        assert adapter.port == 27017
    
    @patch('database.adapters.MongoClient')
    def test_connect(self, mock_client):
        adapter = MongoDBAdapter(
            host="localhost", port=27017, database="test"
        )
        mock_db = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        
        result = adapter.connect()
        assert result == mock_db


class TestAdapterFactory:
    """Test adapter factory function"""
    
    def test_create_postgresql_adapter(self):
        adapter = create_database_adapter(
            DatabaseType.POSTGRESQL,
            host="localhost", port=5432, database="test",
            user="user", password="pass"
        )
        assert isinstance(adapter, PostgreSQLAdapter)
    
    def test_create_mysql_adapter(self):
        adapter = create_database_adapter(
            DatabaseType.MYSQL,
            host="localhost", port=3306, database="test",
            user="user", password="pass"
        )
        assert isinstance(adapter, MySQLAdapter)
    
    def test_create_sqlite_adapter(self):
        adapter = create_database_adapter(
            DatabaseType.SQLITE,
            database_path=":memory:"
        )
        assert isinstance(adapter, SQLiteAdapter)
    
    def test_create_mongodb_adapter(self):
        adapter = create_database_adapter(
            DatabaseType.MONGODB,
            host="localhost", port=27017, database="test"
        )
        assert isinstance(adapter, MongoDBAdapter)
    
    def test_invalid_adapter_type(self):
        with pytest.raises(ValueError):
            create_database_adapter(DatabaseType.DUCKDB, database_path=":memory:")

