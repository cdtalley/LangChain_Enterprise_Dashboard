"""
Core Module Integration Tests
==============================
Tests for core application modules to ensure they work correctly.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestImports:
    """Test that all core modules can be imported"""
    
    def test_agents_import(self):
        from agents import MultiAgentSystem
        assert MultiAgentSystem is not None
    
    def test_advanced_rag_import(self):
        from advanced_rag import AdvancedRAGSystem
        assert AdvancedRAGSystem is not None
    
    def test_model_registry_import(self):
        from model_registry import ModelRegistryManager
        assert ModelRegistryManager is not None
    
    def test_ab_testing_import(self):
        from ab_testing import ABTestingFramework
        assert ABTestingFramework is not None
    
    def test_experiment_tracking_import(self):
        from experiment_tracking import ExperimentTracking
        assert ExperimentTracking is not None
    
    def test_model_monitoring_import(self):
        from model_monitoring import ModelMonitoring
        assert ModelMonitoring is not None


class TestMultiAgentSystem:
    """Test MultiAgentSystem initialization and basic functionality"""
    
    def test_init(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        assert system is not None
        assert hasattr(system, 'agents')
        assert hasattr(system, 'tools')
    
    def test_get_agent_list(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        agent_list = system.get_agent_list()
        assert isinstance(agent_list, list)
    
    def test_get_system_metrics(self):
        from agents import MultiAgentSystem
        system = MultiAgentSystem()
        metrics = system.get_system_metrics()
        assert isinstance(metrics, dict)
        assert "total_tasks" in metrics


class TestAdvancedRAGSystem:
    """Test AdvancedRAGSystem initialization"""
    
    def test_init(self):
        from advanced_rag import AdvancedRAGSystem
        rag = AdvancedRAGSystem()
        assert rag is not None
        assert hasattr(rag, 'embeddings')
        assert hasattr(rag, 'documents')
    
    def test_get_document_summary(self):
        from advanced_rag import AdvancedRAGSystem
        rag = AdvancedRAGSystem()
        summary = rag.get_document_summary()
        assert isinstance(summary, dict)
        assert "total_documents" in summary


class TestModelRegistry:
    """Test ModelRegistryManager"""
    
    def test_init(self):
        from model_registry import ModelRegistryManager
        registry = ModelRegistryManager()
        assert registry is not None
    
    def test_list_models(self):
        from model_registry import ModelRegistryManager
        registry = ModelRegistryManager()
        models = registry.list_models()
        assert isinstance(models, list)


class TestABTesting:
    """Test ABTestingFramework"""
    
    def test_init(self):
        from ab_testing import ABTestingFramework
        framework = ABTestingFramework()
        assert framework is not None
    
    def test_create_experiment(self):
        from ab_testing import ABTestingFramework, ExperimentConfig, MetricType
        framework = ABTestingFramework()
        
        config = ExperimentConfig(
            name="test_exp",
            description="Test",
            metric=MetricType.CONVERSION_RATE,
            target_improvement=0.1
        )
        
        experiment = framework.create_experiment(config)
        assert experiment is not None


class TestConfig:
    """Test configuration management"""
    
    def test_config_import(self):
        from config import Config
        assert Config is not None
        assert hasattr(Config, 'APP_NAME')
        assert hasattr(Config, 'DATABASE_URL')
    
    def test_config_validation(self):
        from config import Config
        result = Config.validate_config()
        assert isinstance(result, bool)

