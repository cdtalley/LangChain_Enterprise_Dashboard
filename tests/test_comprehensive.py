"""
Comprehensive Test Suite
========================
Production-grade tests covering all critical functionality.
"""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestDatabaseAdapters:
    """Test database adapter functionality"""
    
    def test_sqlite_adapter_creation(self):
        from database.adapters import create_database_adapter, DatabaseType
        adapter = create_database_adapter(
            DatabaseType.SQLITE,
            database_path=":memory:"
        )
        assert adapter is not None
        assert adapter.health_check() is True
        adapter.close()
    
    def test_sqlite_query_execution(self):
        from database.adapters import create_database_adapter, DatabaseType
        adapter = create_database_adapter(
            DatabaseType.SQLITE,
            database_path=":memory:"
        )
        adapter.connect()
        
        # Create test table
        adapter.execute_query(
            "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
        )
        
        # Insert data
        adapter.execute_transaction([
            ("INSERT INTO test (name) VALUES (?)", {"name": "test1"}),
            ("INSERT INTO test (name) VALUES (?)", {"name": "test2"})
        ])
        
        # Query data
        results = adapter.execute_query("SELECT * FROM test")
        assert len(results) == 2
        
        adapter.close()
    
    def test_postgresql_adapter_interface(self):
        from database.adapters import PostgreSQLAdapter
        # Test interface without actual connection
        adapter = PostgreSQLAdapter(
            host="localhost",
            port=5432,
            database="test",
            user="test",
            password="test"
        )
        assert adapter.host == "localhost"
        assert adapter.port == 5432


class TestConnectionManager:
    """Test database connection manager"""
    
    def test_manager_initialization(self):
        from database.connection_manager import DatabaseManager
        manager = DatabaseManager("sqlite:///:memory:")
        assert manager is not None
        assert manager.engine is not None
        manager.close()
    
    def test_session_context_manager(self):
        from database.connection_manager import DatabaseManager
        manager = DatabaseManager("sqlite:///:memory:")
        
        with manager.get_session() as session:
            assert session is not None
        
        manager.close()
    
    def test_health_check(self):
        from database.connection_manager import DatabaseManager
        manager = DatabaseManager("sqlite:///:memory:")
        health = manager.health_check()
        assert health["status"] == "healthy"
        manager.close()


class TestMultiAgentSystem:
    """Comprehensive tests for MultiAgentSystem"""
    
    def test_initialization(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        assert system is not None
        assert hasattr(system, 'agents')
        assert hasattr(system, 'tools')
        assert isinstance(system.agents, dict)
        assert isinstance(system.tools, list)
    
    def test_agent_list(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        agents = system.get_agent_list()
        assert isinstance(agents, list)
        assert len(agents) > 0
    
    def test_intelligent_routing(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        
        # Test research query routing
        research_query = "What are the latest trends in AI?"
        agent = system.intelligent_agent_routing(research_query)
        assert agent in system.agents
        
        # Test code query routing
        code_query = "Write Python code to analyze this data"
        agent = system.intelligent_agent_routing(code_query)
        assert agent in system.agents
    
    def test_agent_execution(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        
        if system.agents:
            agent_name = list(system.agents.keys())[0]
            result = system.run_agent(agent_name, "Hello, test query")
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_collaborative_task(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        
        results = system.collaborative_task("Test collaborative task")
        assert isinstance(results, dict)
        assert "_metadata" in results
    
    def test_system_metrics(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        metrics = system.get_system_metrics()
        assert isinstance(metrics, dict)
        assert "total_tasks" in metrics
        assert "successful_tasks" in metrics
    
    def test_agent_capabilities(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        capabilities = system.get_agent_capabilities()
        assert isinstance(capabilities, dict)
        for agent_name, caps in capabilities.items():
            assert "description" in caps
            assert "tools" in caps
            assert "strengths" in caps


class TestAdvancedRAGSystem:
    """Comprehensive tests for AdvancedRAGSystem"""
    
    def test_initialization(self):
        from advanced_rag import AdvancedRAGSystem
        rag = AdvancedRAGSystem()
        assert rag is not None
        assert hasattr(rag, 'embeddings')
        assert hasattr(rag, 'documents')
    
    def test_document_summary_empty(self):
        from advanced_rag import AdvancedRAGSystem
        rag = AdvancedRAGSystem()
        summary = rag.get_document_summary()
        assert summary["total_documents"] == 0
        assert summary["total_chunks"] == 0
    
    def test_query_classification(self):
        from advanced_rag import AdvancedRAGSystem
        rag = AdvancedRAGSystem()
        
        factual_query = "What is the capital of France?"
        query_type = rag._classify_query(factual_query)
        assert query_type in ["factual", "conceptual", "analytical"]
        
        conceptual_query = "Why does this happen?"
        query_type = rag._classify_query(conceptual_query)
        assert query_type in ["factual", "conceptual", "analytical"]
    
    def test_chunk_analytics_empty(self):
        from advanced_rag import AdvancedRAGSystem
        rag = AdvancedRAGSystem()
        analytics = rag.get_chunk_analytics()
        assert analytics["total_chunks"] == 0
        assert isinstance(analytics["chunk_strategies"], dict)


class TestModelRegistry:
    """Test ModelRegistryManager"""
    
    def test_initialization(self):
        from model_registry import ModelRegistryManager
        registry = ModelRegistryManager()
        assert registry is not None
    
    def test_list_models_empty(self):
        from model_registry import ModelRegistryManager
        registry = ModelRegistryManager()
        models = registry.list_models()
        assert isinstance(models, list)
    
    def test_register_model(self):
        from model_registry import ModelRegistryManager, ModelType, ModelStage
        from sklearn.linear_model import LogisticRegression
        import numpy as np
        
        registry = ModelRegistryManager()
        model = LogisticRegression()
        model.fit(np.random.randn(10, 5), np.random.randint(0, 2, 10))
        
        model_id = registry.register_model(
            model=model,
            name="test_model",
            version="1.0.0",
            model_type=ModelType.CLASSIFICATION,
            description="Test model",
            author="Test",
            performance_metrics={"accuracy": 0.95},
            hyperparameters={"learning_rate": 0.01},
            stage=ModelStage.STAGING
        )
        assert model_id is not None
        
        models = registry.list_models()
        assert len(models) > 0


class TestABTesting:
    """Test ABTestingFramework"""
    
    def test_initialization(self):
        from ab_testing import ABTestingFramework
        framework = ABTestingFramework()
        assert framework is not None
    
    def test_create_experiment(self):
        from ab_testing import ABTestingFramework, ExperimentConfig, MetricType
        framework = ABTestingFramework()
        
        config = ExperimentConfig(
            name="test_experiment",
            description="Test experiment",
            hypothesis="Treatment will improve conversion",
            metric_name="conversion_rate",
            metric_type=MetricType.CONVERSION_RATE,
            baseline_model="baseline_v1",
            treatment_model="treatment_v1",
            traffic_split=0.5,
            min_sample_size=1000,
            max_duration_days=7,
            significance_level=0.05
        )
        
        exp_id = framework.create_experiment(config)
        assert exp_id is not None
    
    def test_sample_size_calculation(self):
        from ab_testing import ABTestingFramework
        framework = ABTestingFramework()
        
        sample_size = framework.calculate_sample_size(0.5, 0.05)
        assert isinstance(sample_size, int)
        assert sample_size > 0


class TestExperimentTracking:
    """Test ExperimentTracking"""
    
    def test_initialization(self):
        from experiment_tracking import ExperimentTracking
        tracking = ExperimentTracking()
        assert tracking is not None
    
    def test_start_run(self):
        from experiment_tracking import ExperimentTracking
        tracking = ExperimentTracking()
        
        run_id = tracking.start_run("test_experiment", "test_run")
        assert run_id is not None
    
    def test_log_parameters(self):
        from experiment_tracking import ExperimentTracking
        tracking = ExperimentTracking()
        
        run_id = tracking.start_run("test_experiment", "test_run")
        tracking.log_params(run_id, {"param1": "value1", "param2": 42})
        
        runs = tracking.search_runs(experiment_name="test_experiment")
        assert len(runs) > 0


class TestModelMonitoring:
    """Test ModelMonitoring"""
    
    def test_initialization(self):
        from model_monitoring import ModelMonitoring
        monitoring = ModelMonitoring()
        assert monitoring is not None
    
    def test_log_performance(self):
        from model_monitoring import ModelMonitoring
        monitoring = ModelMonitoring()
        
        monitoring.log_performance(
            "test_model",
            "1.0.0",
            "accuracy",
            0.95,
            1000
        )
        
        # Should not raise exception
        assert True


class TestConfig:
    """Test configuration management"""
    
    def test_config_values(self):
        from config import Config
        assert Config.APP_NAME is not None
        assert Config.DATABASE_URL is not None
        assert isinstance(Config.MAX_TOKENS, int)
        assert isinstance(Config.TEMPERATURE, float)
    
    def test_config_methods(self):
        from config import Config
        db_config = Config.get_database_config()
        assert isinstance(db_config, dict)
        assert "url" in db_config
        
        llm_config = Config.get_llm_config()
        assert isinstance(llm_config, dict)
        assert "model_name" in llm_config
    
    def test_config_validation(self):
        from config import Config
        result = Config.validate_config()
        assert isinstance(result, bool)


class TestErrorHandling:
    """Test error handling across modules"""
    
    def test_agent_invalid_query(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        
        # Test with None query
        result = system.run_agent("researcher", None)
        assert "Error" in result or "Invalid" in result
        
        # Test with empty query
        result = system.run_agent("researcher", "")
        assert isinstance(result, str)
    
    def test_rag_no_documents(self):
        from advanced_rag import AdvancedRAGSystem
        rag = AdvancedRAGSystem()
        
        result = rag.query_documents("test query")
        assert "error" in result or "No documents" in result.get("error", "")
    
    def test_database_adapter_error_handling(self):
        from database.adapters import create_database_adapter, DatabaseType
        
        adapter = create_database_adapter(
            DatabaseType.SQLITE,
            database_path=":memory:"
        )
        
        # Test invalid query
        try:
            adapter.execute_query("INVALID SQL QUERY")
        except Exception:
            pass  # Expected to raise
        
        adapter.close()


class TestCodeExecutor:
    """Test secure code executor"""
    
    def test_code_executor_initialization(self):
        from agents import SecureCodeExecutorTool
        executor = SecureCodeExecutorTool()
        assert executor is not None
    
    def test_safe_code_execution(self):
        from agents import SecureCodeExecutorTool
        executor = SecureCodeExecutorTool()
        
        safe_code = """
result = 2 + 2
print(f"Result: {result}")
"""
        result = executor._run(safe_code)
        assert "Result: 4" in result or "Execution completed" in result
    
    def test_unsafe_code_blocking(self):
        from agents import SecureCodeExecutorTool
        executor = SecureCodeExecutorTool()
        
        unsafe_code = "import os; os.remove('test.txt')"
        result = executor._run(unsafe_code)
        assert "Security Error" in result or "Blocked" in result
    
    def test_execution_stats(self):
        from agents import SecureCodeExecutorTool
        executor = SecureCodeExecutorTool()
        
        executor._run("print('test')")
        stats = executor.get_stats()
        assert stats["total_executions"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

