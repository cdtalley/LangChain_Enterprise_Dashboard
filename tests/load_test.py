"""
Load testing for Enterprise LangChain AI Workbench
==================================================
"""

from locust import HttpUser, task, between
import json
import random


class WorkbenchUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a simulated user starts"""
        # Test health endpoint first
        self.client.get("/health")
    
    @task(3)
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        self.client.get("/health")
    
    @task(2)
    def test_metrics_endpoint(self):
        """Test the metrics endpoint"""
        self.client.get("/metrics")
    
    @task(1)
    def test_agents_list(self):
        """Test listing available agents"""
        self.client.get("/agents")
    
    @task(5)
    def test_query_processing(self):
        """Test query processing with different agents"""
        agents = ["researcher", "coder", "analyst"]
        queries = [
            "What is the capital of France?",
            "Calculate the square root of 144",
            "Analyze the trend in AI adoption",
            "Write a Python function to sort a list",
            "Research the latest developments in quantum computing"
        ]
        
        payload = {
            "query": random.choice(queries),
            "agent": random.choice(agents)
        }
        
        self.client.post(
            "/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
    
    @task(2)
    def test_document_upload(self):
        """Test document upload simulation"""
        # Simulate document upload
        files = {
            'file': ('test_document.txt', 'This is a test document for processing.', 'text/plain')
        }
        
        self.client.post("/upload", files=files)
    
    @task(1)
    def test_system_status(self):
        """Test system status endpoint"""
        self.client.get("/system/status")


class AdminUser(HttpUser):
    """Simulate admin users with different access patterns"""
    wait_time = between(2, 5)
    weight = 1  # Lower weight than regular users
    
    @task(2)
    def test_admin_metrics(self):
        """Test admin-level metrics"""
        self.client.get("/admin/metrics")
    
    @task(1)
    def test_system_configuration(self):
        """Test system configuration endpoints"""
        self.client.get("/admin/config")
    
    @task(1)
    def test_user_management(self):
        """Test user management endpoints"""
        self.client.get("/admin/users")


class HighVolumeUser(HttpUser):
    """Simulate high-volume API users"""
    wait_time = between(0.1, 0.5)  # Very frequent requests
    weight = 0.5  # Even lower weight
    
    @task
    def rapid_fire_queries(self):
        """Rapid succession of queries"""
        for i in range(5):
            payload = {
                "query": f"Quick query #{i}",
                "agent": "analyst"
            }
            self.client.post("/query", json=payload) 