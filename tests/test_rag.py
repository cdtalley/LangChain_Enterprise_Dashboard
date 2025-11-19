"""
RAG System Tests
================
Tests for advanced RAG system functionality.
"""

import pytest
import tempfile
from pathlib import Path

from advanced_rag import AdvancedRAGSystem


class TestAdvancedRAGSystem:
    """Test advanced RAG system."""
    
    def test_initialization(self):
        """Test RAG system initialization."""
        rag = AdvancedRAGSystem()
        assert rag is not None
        assert hasattr(rag, 'embeddings')
        assert hasattr(rag, 'llm')
    
    def test_document_summary(self):
        """Test document summary."""
        rag = AdvancedRAGSystem()
        summary = rag.get_document_summary()
        assert isinstance(summary, dict)
        assert "total_documents" in summary
    
    def test_chunk_analytics(self):
        """Test chunk analytics."""
        rag = AdvancedRAGSystem()
        analytics = rag.get_chunk_analytics()
        assert isinstance(analytics, dict)
        assert "total_chunks" in analytics
    
    def test_semantic_search_empty(self):
        """Test semantic search with no documents."""
        rag = AdvancedRAGSystem()
        results = rag.semantic_search("test query")
        assert isinstance(results, list)
        assert len(results) == 0
    
    def test_query_classification(self):
        """Test query classification."""
        rag = AdvancedRAGSystem()
        
        # Factual query
        query_type = rag._classify_query("What is Python?")
        assert query_type in ["factual", "conceptual", "analytical"]
        
        # Conceptual query
        query_type = rag._classify_query("Why does this happen?")
        assert query_type in ["factual", "conceptual", "analytical"]
        
        # Analytical query
        query_type = rag._classify_query("Analyze the trends")
        assert query_type in ["factual", "conceptual", "analytical"]

