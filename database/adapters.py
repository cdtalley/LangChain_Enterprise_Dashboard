"""
Database Adapter Layer
======================
Production-ready database abstraction supporting multiple backends.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    DUCKDB = "duckdb"


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters"""
    
    @abstractmethod
    def connect(self) -> Any:
        """Establish database connection"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        pass
    
    @abstractmethod
    def execute_transaction(self, queries: List[tuple]) -> bool:
        """Execute multiple queries in a transaction"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close database connection"""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """Check database health"""
        pass


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter"""
    
    def __init__(self, host: str, port: int, database: str, 
                 user: str, password: str, **kwargs):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection_params = kwargs
        self._conn = None
        self._engine = None
    
    def connect(self):
        try:
            from sqlalchemy import create_engine, text
            from sqlalchemy.pool import QueuePool
            
            connection_string = (
                f"postgresql://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )
            
            self._engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                **self.connection_params
            )
            self._conn = self._engine.connect()
            logger.info(f"Connected to PostgreSQL: {self.database}")
            return self._conn
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            raise
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        if not self._conn:
            self.connect()
        
        try:
            from sqlalchemy import text
            result = self._conn.execute(text(query), params or {})
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_transaction(self, queries: List[tuple]) -> bool:
        if not self._conn:
            self.connect()
        
        trans = self._conn.begin()
        try:
            from sqlalchemy import text
            for query, params in queries:
                self._conn.execute(text(query), params or {})
            trans.commit()
            return True
        except Exception as e:
            trans.rollback()
            logger.error(f"Transaction failed: {e}")
            return False
    
    def close(self):
        if self._conn:
            self._conn.close()
        if self._engine:
            self._engine.dispose()
    
    def health_check(self) -> bool:
        try:
            result = self.execute_query("SELECT 1")
            return len(result) > 0
        except:
            return False


class MySQLAdapter(DatabaseAdapter):
    """MySQL database adapter"""
    
    def __init__(self, host: str, port: int, database: str,
                 user: str, password: str, **kwargs):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection_params = kwargs
        self._conn = None
        self._engine = None
    
    def connect(self):
        try:
            from sqlalchemy import create_engine, text
            
            connection_string = (
                f"mysql+pymysql://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )
            
            self._engine = create_engine(
                connection_string,
                pool_pre_ping=True,
                **self.connection_params
            )
            self._conn = self._engine.connect()
            logger.info(f"Connected to MySQL: {self.database}")
            return self._conn
        except Exception as e:
            logger.error(f"MySQL connection failed: {e}")
            raise
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        if not self._conn:
            self.connect()
        
        try:
            from sqlalchemy import text
            result = self._conn.execute(text(query), params or {})
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_transaction(self, queries: List[tuple]) -> bool:
        if not self._conn:
            self.connect()
        
        trans = self._conn.begin()
        try:
            from sqlalchemy import text
            for query, params in queries:
                self._conn.execute(text(query), params or {})
            trans.commit()
            return True
        except Exception as e:
            trans.rollback()
            logger.error(f"Transaction failed: {e}")
            return False
    
    def close(self):
        if self._conn:
            self._conn.close()
        if self._engine:
            self._engine.dispose()
    
    def health_check(self) -> bool:
        try:
            result = self.execute_query("SELECT 1")
            return len(result) > 0
        except:
            return False


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter"""
    
    def __init__(self, database_path: str, **kwargs):
        self.database_path = database_path
        self.connection_params = kwargs
        self._conn = None
        self._engine = None
    
    def connect(self):
        try:
            from sqlalchemy import create_engine, text
            
            connection_string = f"sqlite:///{self.database_path}"
            self._engine = create_engine(
                connection_string,
                pool_pre_ping=True,
                **self.connection_params
            )
            self._conn = self._engine.connect()
            logger.info(f"Connected to SQLite: {self.database_path}")
            return self._conn
        except Exception as e:
            logger.error(f"SQLite connection failed: {e}")
            raise
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        if not self._conn:
            self.connect()
        
        try:
            from sqlalchemy import text
            result = self._conn.execute(text(query), params or {})
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_transaction(self, queries: List[tuple]) -> bool:
        if not self._conn:
            self.connect()
        
        trans = self._conn.begin()
        try:
            from sqlalchemy import text
            for query, params in queries:
                self._conn.execute(text(query), params or {})
            trans.commit()
            return True
        except Exception as e:
            trans.rollback()
            logger.error(f"Transaction failed: {e}")
            return False
    
    def close(self):
        if self._conn:
            self._conn.close()
        if self._engine:
            self._engine.dispose()
    
    def health_check(self) -> bool:
        try:
            result = self.execute_query("SELECT 1")
            return len(result) > 0
        except:
            return False


class MongoDBAdapter(DatabaseAdapter):
    """MongoDB database adapter"""
    
    def __init__(self, host: str, port: int, database: str,
                 user: Optional[str] = None, password: Optional[str] = None, **kwargs):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection_params = kwargs
        self._client = None
        self._db = None
    
    def connect(self):
        try:
            from pymongo import MongoClient
            
            if self.user and self.password:
                connection_string = (
                    f"mongodb://{self.user}:{self.password}@"
                    f"{self.host}:{self.port}/{self.database}"
                )
            else:
                connection_string = f"mongodb://{self.host}:{self.port}/"
            
            self._client = MongoClient(connection_string, **self.connection_params)
            self._db = self._client[self.database]
            logger.info(f"Connected to MongoDB: {self.database}")
            return self._db
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise
    
    def execute_query(self, query: Dict[str, Any], collection: str = "default") -> List[Dict[str, Any]]:
        """Execute MongoDB query. Note: collection parameter is required for MongoDB."""
        if not self._db:
            self.connect()
        
        try:
            collection_obj = self._db[collection]
            results = list(collection_obj.find(query))
            for result in results:
                result.pop('_id', None)
            return results
        except Exception as e:
            logger.error(f"MongoDB query execution failed: {e}")
            raise
    
    def execute_transaction(self, operations: List[tuple]) -> bool:
        """Execute MongoDB transaction. Operations format: (collection, operation, data)."""
        if not self._db:
            self.connect()
        
        if not self._client:
            logger.error("MongoDB client not initialized")
            return False
        
        try:
            with self._client.start_session() as session:
                with session.start_transaction():
                    for operation_tuple in operations:
                        if len(operation_tuple) != 3:
                            raise ValueError("Each operation must be (collection, operation, data)")
                        collection, operation, data = operation_tuple
                        collection_obj = self._db[collection]
                        
                        if operation == "insert":
                            collection_obj.insert_one(data, session=session)
                        elif operation == "update":
                            if "filter" not in data or "update" not in data:
                                raise ValueError("Update operation requires 'filter' and 'update' keys")
                            collection_obj.update_one(data["filter"], data["update"], session=session)
                        elif operation == "delete":
                            if "filter" not in data:
                                raise ValueError("Delete operation requires 'filter' key")
                            collection_obj.delete_one(data["filter"], session=session)
                        else:
                            raise ValueError(f"Unknown operation: {operation}")
            return True
        except Exception as e:
            logger.error(f"MongoDB transaction failed: {e}")
            return False
    
    def close(self):
        if self._client:
            self._client.close()
    
    def health_check(self) -> bool:
        """Check MongoDB connection health."""
        if not self._client:
            return False
        try:
            self._client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"MongoDB health check failed: {e}")
            return False


def create_database_adapter(db_type: DatabaseType, **kwargs) -> DatabaseAdapter:
    """Factory function to create appropriate database adapter"""
    adapters = {
        DatabaseType.POSTGRESQL: PostgreSQLAdapter,
        DatabaseType.MYSQL: MySQLAdapter,
        DatabaseType.SQLITE: SQLiteAdapter,
        DatabaseType.MONGODB: MongoDBAdapter,
    }
    
    adapter_class = adapters.get(db_type)
    if not adapter_class:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return adapter_class(**kwargs)

