"""
Comprehensive test suite for Enterprise LangChain AI Workbench
==============================================================
Demonstrates production-ready testing practices including:
- Unit tests for core functionality
- Integration tests for API endpoints
- Performance tests
- Security tests
- Mock testing for external dependencies
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
import json
import tempfile
import os
from datetime import datetime

# Import modules to test
from enterprise_features import app, EnterpriseMonitor, monitor
from agents import MultiAgentSystem, SecureCodeExecutorTool
from advanced_rag import AdvancedRAGSystem, LocalEmbeddings

# Test client
client = TestClient(app)

class TestEnterpriseMonitor:
    """Test suite for EnterpriseMonitor class"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.monitor = EnterpriseMonitor()
    
    def test_monitor_initialization(self):
        """Test monitor initializes with correct default values"""
        assert self.monitor.metrics["total_queries"] == 0
        assert self.monitor.metrics["successful_queries"] == 0
        assert self.monitor.metrics["failed_queries"] == 0
        assert self.monitor.metrics["avg_response_time"] == 0
        assert isinstance(self.monitor.query_cache, dict)
    
    def test_log_successful_query(self):
        """Test logging a successful query"""
        self.monitor.log_query("test query", 1.5, True, "researcher")
        
        assert self.monitor.metrics["total_queries"] == 1
        assert self.monitor.metrics["successful_queries"] == 1
        assert self.monitor.metrics["failed_queries"] == 0
        assert self.monitor.metrics["avg_response_time"] == 1.5
    
    def test_log_failed_query(self):
        """Test logging a failed query"""
        self.monitor.log_query("test query", 2.0, False, "coder")
        
        assert self.monitor.metrics["total_queries"] == 1
        assert self.monitor.metrics["successful_queries"] == 0
        assert self.monitor.metrics["failed_queries"] == 1
        assert self.monitor.metrics["avg_response_time"] == 2.0
    
    def test_cache_functionality(self):
        """Test query caching works correctly"""
        query = "test query"
        agent = "researcher"
        response = "test response"
        
        # Should be cache miss initially
        cached = self.monitor.get_cached_response(query, agent)
        assert cached is None
        assert self.monitor.metrics["cache_misses"] == 1
        
        # Cache the response
        self.monitor.cache_response(query, agent, response)
        
        # Should be cache hit now
        cached = self.monitor.get_cached_response(query, agent)
        assert cached == response
        assert self.monitor.metrics["cache_hits"] == 1
    
    def test_system_status(self):
        """Test system status generation"""
        # Add some metrics
        self.monitor.log_query("query1", 1.0, True, "researcher")
        self.monitor.log_query("query2", 2.0, True, "coder")
        
        status = self.monitor.get_system_status()
        
        assert status.status == "healthy"
        assert status.total_queries == 2
        assert status.success_rate == 100.0
        assert status.avg_response_time == 1.5
        assert len(status.active_agents) == 3

class TestSecureCodeExecutor:
    """Test suite for SecureCodeExecutorTool"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.executor = SecureCodeExecutorTool()
    
    def test_safe_code_execution(self):
        """Test execution of safe code"""
        safe_code = "print('Hello, World!')\nresult = 2 + 2"
        result = self.executor._run(safe_code)
        
        assert "Hello, World!" in result
        assert "✅ Execution completed" in result
        assert self.executor.execution_stats["successful_executions"] == 1
    
    def test_dangerous_code_blocking(self):
        """Test that dangerous code is blocked"""
        dangerous_codes = [
            "import os",
            "import subprocess",
            "eval('malicious_code')",
            "exec('dangerous_operation')",
            "open('/etc/passwd', 'r')",
        ]
        
        for code in dangerous_codes:
            result = self.executor._run(code)
            assert "🚫 Security Error" in result
        
        assert self.executor.execution_stats["blocked_operations"] >= len(dangerous_codes)
    
    def test_math_operations(self):
        """Test mathematical operations work correctly"""
        math_code = """
import math
result = math.sqrt(16) + math.pi
print(f"Result: {result}")
"""
        result = self.executor._run(math_code)
        assert "Result:" in result
        assert "✅ Execution completed" in result
    
    def test_pandas_operations(self):
        """Test pandas operations work correctly"""
        pandas_code = """
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(df.sum())
"""
        result = self.executor._run(pandas_code)
        assert "✅ Execution completed" in result
    
    def test_execution_statistics(self):
        """Test execution statistics are tracked correctly"""
        initial_stats = self.executor.get_stats()
        
        # Execute some code
        self.executor._run("print('test')")
        self.executor._run("print('test2')")
        self.executor._run("import os")  # This should be blocked
        
        final_stats = self.executor.get_stats()
        
        assert final_stats["total_executions"] == initial_stats["total_executions"] + 3
        assert final_stats["successful_executions"] == initial_stats["successful_executions"] + 2
        assert final_stats["blocked_operations"] == initial_stats["blocked_operations"] + 1

class TestLocalEmbeddings:
    """Test suite for LocalEmbeddings"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.embeddings = LocalEmbeddings()
    
    def test_embed_single_query(self):
        """Test embedding a single query"""
        text = "This is a test query"
        embedding = self.embeddings.embed_query(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)
    
    def test_embed_multiple_documents(self):
        """Test embedding multiple documents"""
        texts = ["Document 1", "Document 2", "Document 3"]
        embeddings = self.embeddings.embed_documents(texts)
        
        assert isinstance(embeddings, list)
        assert len(embeddings) == len(texts)
        assert all(isinstance(emb, list) for emb in embeddings)
    
    @pytest.mark.asyncio
    async def test_async_embedding(self):
        """Test async embedding methods"""
        text = "Async test query"
        
        # Test async query embedding
        embedding = await self.embeddings.aembed_query(text)
        assert isinstance(embedding, list)
        
        # Test async document embedding
        texts = ["Doc 1", "Doc 2"]
        embeddings = await self.embeddings.aembed_documents(texts)
        assert len(embeddings) == 2

class TestAPIEndpoints:
    """Test suite for FastAPI endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "Enterprise LangChain AI Workbench API" in data["message"]
        assert data["version"] == "2.0.0"
        assert "features" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "uptime" in data
        assert "total_queries" in data
        assert "active_agents" in data
    
    def test_agents_list(self):
        """Test agents listing endpoint"""
        response = client.get("/api/v1/agents")
        assert response.status_code == 200
        
        data = response.json()
        assert "agents" in data
        agents = data["agents"]
        assert len(agents) == 3
        
        agent_names = [agent["name"] for agent in agents]
        assert "researcher" in agent_names
        assert "coder" in agent_names
        assert "analyst" in agent_names
    
    @patch('enterprise_features.multi_agent')
    def test_query_processing(self, mock_multi_agent):
        """Test query processing endpoint"""
        # Mock the agent response
        mock_multi_agent.run_agent.return_value = "Test response from agent"
        
        query_data = {
            "query": "Test query",
            "agent_type": "researcher"
        }
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.post(
            "/api/v1/query", 
            json=query_data, 
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "query_id" in data
        assert data["response"] == "Test response from agent"
        assert data["agent_used"] == "researcher"
        assert "processing_time" in data
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        headers = {"Authorization": "Bearer test-token"}
        response = client.get("/api/v1/metrics", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "metrics" in data
        assert "cache_info" in data
        assert "timestamp" in data

class TestPerformance:
    """Performance tests for critical components"""
    
    def test_embedding_performance(self):
        """Test embedding performance meets requirements"""
        embeddings = LocalEmbeddings()
        text = "Performance test query " * 50  # Longer text
        
        start_time = time.time()
        embedding = embeddings.embed_query(text)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < 5.0  # Should complete within 5 seconds
        assert len(embedding) > 0
    
    def test_code_execution_performance(self):
        """Test code execution performance"""
        executor = SecureCodeExecutorTool()
        code = """
import pandas as pd
import numpy as np
data = np.random.randn(1000, 10)
df = pd.DataFrame(data)
result = df.describe()
print("Performance test completed")
"""
        
        start_time = time.time()
        result = executor._run(code)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < 10.0  # Should complete within 10 seconds
        assert "✅ Execution completed" in result
    
    def test_concurrent_requests(self):
        """Test handling of concurrent API requests"""
        def make_request():
            response = client.get("/health")
            return response.status_code
        
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [future.result() for future in futures]
        
        # All requests should succeed
        assert all(status == 200 for status in results)

class TestSecurity:
    """Security tests for the application"""
    
    def test_code_injection_prevention(self):
        """Test prevention of code injection attacks"""
        executor = SecureCodeExecutorTool()
        
        injection_attempts = [
            "__import__('os').system('rm -rf /')",
            "exec(open('/etc/passwd').read())",
            "eval('__import__(\"os\").system(\"whoami\")')",
            "import subprocess; subprocess.call(['ls', '/'])",
        ]
        
        for attempt in injection_attempts:
            result = executor._run(attempt)
            assert "🚫 Security Error" in result
    
    def test_unauthorized_api_access(self):
        """Test that protected endpoints require authentication"""
        # Try to access protected endpoint without token
        response = client.post("/api/v1/query", json={"query": "test"})
        assert response.status_code == 403  # Forbidden
        
        response = client.get("/api/v1/metrics")
        assert response.status_code == 403  # Forbidden
    
    def test_input_validation(self):
        """Test input validation for API endpoints"""
        headers = {"Authorization": "Bearer test-token"}
        
        # Invalid query data
        invalid_data = {"invalid_field": "test"}
        response = client.post(
            "/api/v1/query", 
            json=invalid_data, 
            headers=headers
        )
        assert response.status_code == 422  # Validation error

class TestIntegration:
    """Integration tests for the complete system"""
    
    @patch('enterprise_features.multi_agent')
    def test_end_to_end_query_flow(self, mock_multi_agent):
        """Test complete query processing flow"""
        # Mock agent response
        mock_multi_agent.run_agent.return_value = "Integration test response"
        
        # Make query request
        query_data = {
            "query": "What are the latest AI trends?",
            "agent_type": "auto",
            "context": {"source": "integration_test"}
        }
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.post(
            "/api/v1/query", 
            json=query_data, 
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "query_id" in data
        assert "response" in data
        assert "agent_used" in data
        assert "processing_time" in data
        assert "metadata" in data
        
        # Verify agent was called correctly
        mock_multi_agent.run_agent.assert_called_once()
    
    def test_system_resilience(self):
        """Test system handles errors gracefully"""
        # Test health endpoint during high load
        responses = []
        for _ in range(50):
            response = client.get("/health")
            responses.append(response.status_code)
        
        # Should maintain 100% availability
        success_rate = sum(1 for r in responses if r == 200) / len(responses)
        assert success_rate >= 0.95  # At least 95% success rate

# Pytest configuration
pytest_plugins = ["pytest_asyncio"]

if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([
        __file__, 
        "-v", 
        "--cov=enterprise_features", 
        "--cov=agents", 
        "--cov=advanced_rag",
        "--cov-report=html",
        "--cov-report=term-missing"
    ]) 