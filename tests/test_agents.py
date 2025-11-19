"""
Agent System Tests
==================
Tests for multi-agent system functionality.
"""

import pytest
from unittest.mock import Mock, patch

from agents import MultiAgentSystem


class TestMultiAgentSystem:
    """Test multi-agent system."""
    
    def test_initialization(self):
        """Test agent system initialization."""
        system = MultiAgentSystem()
        assert system is not None
        assert hasattr(system, 'agents')
        assert hasattr(system, 'tools')
    
    def test_agent_list(self):
        """Test getting agent list."""
        system = MultiAgentSystem()
        agents = system.get_agent_list()
        assert isinstance(agents, list)
    
    def test_system_metrics(self):
        """Test system metrics."""
        system = MultiAgentSystem()
        metrics = system.get_system_metrics()
        assert isinstance(metrics, dict)
        assert "total_tasks" in metrics
        assert "successful_tasks" in metrics
    
    def test_agent_capabilities(self):
        """Test agent capabilities."""
        system = MultiAgentSystem()
        capabilities = system.get_agent_capabilities()
        assert isinstance(capabilities, dict)
    
    def test_intelligent_routing(self):
        """Test intelligent agent routing."""
        system = MultiAgentSystem()
        
        # Test research query
        agent = system.intelligent_agent_routing("What is machine learning?")
        assert agent in system.get_agent_list()
        
        # Test code query
        agent = system.intelligent_agent_routing("Write a Python function")
        assert agent in system.get_agent_list()
        
        # Test analysis query
        agent = system.intelligent_agent_routing("Analyze this data")
        assert agent in system.get_agent_list()
    
    def test_cleanup(self):
        """Test cleanup method."""
        system = MultiAgentSystem()
        system.cleanup()  # Should not raise exception

