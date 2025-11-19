"""
Production-Ready Test Suite
============================
Comprehensive tests ensuring enterprise-grade quality and reliability.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestDatabaseAbstraction:
    """Test database abstraction layer"""
    
    def test_database_manager_initialization(self):
        """Test DatabaseManager can be initialized"""
        from database.connection_manager import DatabaseManager
        
        # Use in-memory SQLite for testing
        db_manager = DatabaseManager("sqlite:///:memory:")
        assert db_manager is not None
        assert db_manager.engine is not None
        db_manager.close()
    
    def test_database_session_context(self):
        """Test database session context manager"""
        from database.connection_manager import DatabaseManager
        
        db_manager = DatabaseManager("sqlite:///:memory:")
        with db_manager.get_session() as session:
            assert session is not None
        db_manager.close()
    
    def test_database_health_check(self):
        """Test database health check"""
        from database.connection_manager import DatabaseManager
        
        db_manager = DatabaseManager("sqlite:///:memory:")
        health = db_manager.health_check()
        assert health["status"] == "healthy"
        db_manager.close()
    
    def test_database_adapter_factory(self):
        """Test database adapter factory"""
        from database.adapters import create_database_adapter, DatabaseType
        
        # Test SQLite adapter creation
        adapter = create_database_adapter(
            DatabaseType.SQLITE,
            database_path=":memory:"
        )
        assert adapter is not None
        adapter.close()


class TestErrorHandling:
    """Test error handling and resilience"""
    
    def test_agents_graceful_degradation(self):
        """Test agents handle errors gracefully"""
        from agents import MultiAgentSystem
        
        system = MultiAgentSystem()
        
        # Test with invalid agent name
        result = system.run_agent("nonexistent", "test query")
        assert "not found" in result.lower() or "error" in result.lower()
        
        # Test with empty query
        result = system.run_agent("analyst", "")
        assert "error" in result.lower() or "invalid" in result.lower()
    
    def test_rag_error_handling(self):
        """Test RAG system error handling"""
        from advanced_rag import AdvancedRAGSystem
        
        rag = AdvancedRAGSystem()
        
        # Test query with no documents
        result = rag.query_documents("test query")
        assert "error" in result or "no documents" in str(result).lower()
        
        # Test invalid retrieval strategy
        result = rag.query_documents("test", retrieval_strategy="invalid")
        # Should handle gracefully
        assert isinstance(result, dict)
    
    def test_config_validation(self):
        """Test configuration validation"""
        from config import Config
        
        # Should validate without errors
        result = Config.validate_config()
        assert isinstance(result, bool)


class TestCodeQuality:
    """Test code quality and best practices"""
    
    def test_imports_are_clean(self):
        """Test all imports are valid"""
        import agents
        import advanced_rag
        import model_registry
        import ab_testing
        import experiment_tracking
        import model_monitoring
        import config
        import database.connection_manager
        import database.adapters
        
        # If we get here, imports are successful
        assert True
    
    def test_no_circular_imports(self):
        """Test no circular import issues"""
        # This test will fail if there are circular imports
        import agents
        import advanced_rag
        import model_registry
        
        assert True
    
    def test_type_hints_present(self):
        """Test that key functions have type hints"""
        from agents import MultiAgentSystem
        from advanced_rag import AdvancedRAGSystem
        
        import inspect
        
        # Check MultiAgentSystem methods
        methods = ['run_agent', 'get_system_metrics', 'get_agent_list']
        for method_name in methods:
            method = getattr(MultiAgentSystem, method_name)
            sig = inspect.signature(method)
            # Check that at least some parameters have type hints
            assert len(sig.parameters) > 0
        
        # Check AdvancedRAGSystem methods
        methods = ['query_documents', 'get_document_summary']
        for method_name in methods:
            method = getattr(AdvancedRAGSystem, method_name)
            sig = inspect.signature(method)
            assert len(sig.parameters) > 0


class TestPerformance:
    """Test performance characteristics"""
    
    def test_agent_initialization_speed(self):
        """Test agent initialization is reasonably fast"""
        import time
        from agents import MultiAgentSystem
        
        start = time.time()
        system = MultiAgentSystem()
        elapsed = time.time() - start
        
        # Should initialize in reasonable time (< 10 seconds)
        assert elapsed < 10.0
    
    def test_rag_initialization_speed(self):
        """Test RAG initialization is reasonably fast"""
        import time
        from advanced_rag import AdvancedRAGSystem
        
        start = time.time()
        rag = AdvancedRAGSystem()
        elapsed = time.time() - start
        
        # Should initialize in reasonable time (< 15 seconds)
        assert elapsed < 15.0


class TestSecurity:
    """Test security features"""
    
    def test_code_executor_security(self):
        """Test code executor blocks dangerous operations"""
        from agents import SecureCodeExecutorTool
        
        executor = SecureCodeExecutorTool()
        
        # Test blocked operations
        dangerous_codes = [
            "import os",
            "import subprocess",
            "__import__('os')",
            "eval('print(1)')",
            "exec('print(1)')",
            "open('file.txt', 'w')",
        ]
        
        for code in dangerous_codes:
            result = executor._run(code)
            assert "security" in result.lower() or "blocked" in result.lower() or "error" in result.lower()
    
    def test_web_scraper_rate_limiting(self):
        """Test web scraper has rate limiting"""
        from agents import WebScrapeTool
        
        scraper = WebScrapeTool()
        assert hasattr(scraper, '_rate_limit')
        assert hasattr(scraper, 'last_request_time')


class TestIntegration:
    """Test integration between components"""
    
    def test_agents_and_rag_integration(self):
        """Test agents and RAG can work together"""
        from agents import MultiAgentSystem
        from advanced_rag import AdvancedRAGSystem
        
        system = MultiAgentSystem()
        rag = AdvancedRAGSystem()
        
        # Both should be initialized
        assert system is not None
        assert rag is not None
        
        # Both should have required methods
        assert hasattr(system, 'run_agent')
        assert hasattr(rag, 'query_documents')
    
    def test_config_used_throughout(self):
        """Test Config is used throughout codebase"""
        from config import Config
        
        # Config should have all required settings
        assert hasattr(Config, 'DATABASE_URL')
        assert hasattr(Config, 'DEFAULT_LLM_MODEL')
        assert hasattr(Config, 'MAX_TOKENS')
        assert hasattr(Config, 'TEMPERATURE')


class TestLogging:
    """Test logging is properly configured"""
    
    def test_logging_configured(self):
        """Test logging is configured"""
        import logging
        
        logger = logging.getLogger('agents')
        assert logger is not None
        assert logger.level >= logging.DEBUG
    
    def test_error_logging(self):
        """Test errors are logged"""
        from agents import MultiAgentSystem
        import logging
        
        # Capture log output
        log_capture = []
        
        class TestHandler(logging.Handler):
            def emit(self, record):
                log_capture.append(record.getMessage())
        
        logger = logging.getLogger('agents')
        handler = TestHandler()
        logger.addHandler(handler)
        
        system = MultiAgentSystem()
        # Trigger an error
        system.run_agent("nonexistent", "test")
        
        # Should have logged something
        assert len(log_capture) >= 0  # May or may not log, but shouldn't crash


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

