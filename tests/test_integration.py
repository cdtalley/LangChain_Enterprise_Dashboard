"""
Integration Tests
=================
End-to-end integration tests for the complete system.
"""

import pytest
import tempfile
import os

from agents import MultiAgentSystem
from advanced_rag import AdvancedRAGSystem
from database.connection_manager import DatabaseManager


class TestSystemIntegration:
    """Test system integration."""
    
    def test_agent_and_rag_integration(self):
        """Test agent and RAG system work together."""
        agent_system = MultiAgentSystem()
        rag_system = AdvancedRAGSystem()
        
        assert agent_system is not None
        assert rag_system is not None
    
    def test_database_and_models_integration(self):
        """Test database and models integration."""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        try:
            db_url = f"sqlite:///{path}"
            db_manager = DatabaseManager(database_url=db_url)
            db_manager.create_tables()
            
            # Test that we can use models with database
            with db_manager.get_session() as session:
                from database.models import QueryLog
                log = QueryLog(
                    query_text="Test",
                    response_text="Response"
                )
                session.add(log)
                session.commit()
                
                assert log.id is not None
        finally:
            db_manager.close()
            os.unlink(path)
    
    def test_configuration_loading(self):
        """Test configuration loads correctly."""
        from config import Config
        
        assert Config.APP_NAME is not None
        assert Config.DATABASE_URL is not None
        assert isinstance(Config.MAX_TOKENS, int)

