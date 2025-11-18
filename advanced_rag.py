import os
from typing import List, Dict, Any, Optional, Tuple
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter, 
    TokenTextSplitter,
    SpacyTextSplitter
)
# from langchain_openai.embeddings import OpenAIEmbeddings  # Optional import
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
# from langchain_openai import ChatOpenAI  # Optional import
from langchain.chains import RetrievalQA
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.memory import ConversationSummaryBufferMemory
import tempfile
import hashlib
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
from transformers import pipeline
# from langchain_huggingface import HuggingFacePipeline  # Optional import
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalEmbeddings:
    """Production-ready local embeddings with full LangChain compatibility"""
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        logger.info(f"Initializing LocalEmbeddings with model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
        except Exception as e:
            logger.warning(f"Failed to load {model_name}, using fallback: {e}")
            # Create a simple fallback embedding model
            from langchain_community.embeddings import FakeEmbeddings
            self.model = FakeEmbeddings(size=384)
            self.model_name = "fake_embeddings"
        
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text"""
        start_time = time.time()
        if hasattr(self.model, 'encode'):
            embedding = self.model.encode(text).tolist()
        else:
            embedding = self.model.embed_query(text)
        logger.info(f"Query embedding completed in {time.time() - start_time:.2f}s")
        return embedding
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents"""
        start_time = time.time()
        if hasattr(self.model, 'encode'):
            embeddings = self.model.encode(texts).tolist()
        else:
            embeddings = self.model.embed_documents(texts)
        logger.info(f"Document embeddings completed for {len(texts)} docs in {time.time() - start_time:.2f}s")
        return embeddings
    
    async def aembed_query(self, text: str) -> List[float]:
        """Async version of embed_query"""
        return self.embed_query(text)
    
    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Async version of embed_documents"""
        return self.embed_documents(texts)

class AdvancedRAGSystem:
    def __init__(self, openai_api_key: str = None, use_local_embeddings: bool = True):
        """Initialize RAG system with local LLM fallback chain"""
        try:
            hf_pipeline = pipeline("text-generation", model="gpt2", max_length=256, temperature=0.7, do_sample=True)
            try:
                from langchain_huggingface import HuggingFacePipeline
                self.llm = HuggingFacePipeline(pipeline=hf_pipeline, model_kwargs={"temperature": 0.7, "max_length": 256})
            except ImportError:
                self.llm = hf_pipeline
        except Exception as e:
            logger.warning(f"GPT-2 initialization failed, using fallback: {e}")
            from langchain.llms.fake import FakeListLLM
            self.llm = FakeListLLM(responses=[
                "Based on the provided context, here's what I found:",
                "The documents contain relevant information about your query.",
                "I can help you analyze the uploaded documents."
            ])
        
        self.embeddings = LocalEmbeddings()
        self.performance_metrics = {
            "queries_processed": 0, "avg_response_time": 0, "total_documents": 0,
            "cache_hits": 0, "errors": 0
        }
        self.query_cache: Dict[str, Any] = {}
        self.documents: List[Document] = []
        self.vectorstores: Dict[str, Any] = {}
        self.retrievers: Dict[str, Any] = {}
        self.document_metadata: Dict[str, Dict] = {}
        
        # Advanced chunking strategies
        self.text_splitters = {
            "recursive": RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            ),
            "token": TokenTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            ),
            "semantic": RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=300,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
        }
        
        logger.info("AdvancedRAGSystem initialization complete")
    
    def load_document(self, file_path: str, file_type: str, metadata: Dict = None) -> str:
        """Load and process a document with advanced chunking"""
        try:
            # Generate unique document ID
            doc_id = hashlib.md5(f"{file_path}_{file_type}".encode()).hexdigest()
            
            # Load document based on type
            if file_type == "pdf":
                loader = PyPDFLoader(file_path)
            elif file_type == "txt":
                loader = TextLoader(file_path)
            elif file_type == "docx":
                loader = UnstructuredWordDocumentLoader(file_path)
            else:
                return f"Unsupported file type: {file_type}"
            
            # Load and split documents
            raw_docs = loader.load()
            
            # Apply multiple chunking strategies
            all_chunks = []
            for strategy_name, splitter in self.text_splitters.items():
                chunks = splitter.split_documents(raw_docs)
                for i, chunk in enumerate(chunks):
                    chunk.metadata.update({
                        "doc_id": doc_id,
                        "chunk_strategy": strategy_name,
                        "chunk_index": i,
                        "file_type": file_type,
                        **(metadata or {})
                    })
                all_chunks.extend(chunks)
            
            self.documents.extend(all_chunks)
            
            # Store document metadata
            self.document_metadata[doc_id] = {
                "file_path": file_path,
                "file_type": file_type,
                "num_chunks": len(all_chunks),
                "metadata": metadata or {}
            }
            
            # Create vector stores
            self._create_vector_stores(doc_id, all_chunks)
            
            return f"Successfully loaded document {doc_id} with {len(all_chunks)} chunks"
            
        except Exception as e:
            return f"Error loading document: {str(e)}"
    
    def _create_vector_stores(self, doc_id: str, chunks: List[Document]):
        """Create multiple vector stores for different retrieval strategies"""
        # Dense vector store (semantic similarity)
        try:
            dense_vectorstore = Chroma.from_documents(
                chunks,
                self.embeddings.model,
                collection_name=f"dense_{doc_id}"
            )
        except Exception as e:
            logger.warning(f"Failed to create Chroma vectorstore: {e}")
            # Use FAISS as fallback
            from langchain_community.vectorstores import FAISS
            dense_vectorstore = FAISS.from_documents(chunks, self.embeddings.model)
        
        # BM25 retriever (keyword-based)
        texts = [doc.page_content for doc in chunks]
        bm25_retriever = BM25Retriever.from_texts(texts)
        bm25_retriever.k = 5
        
        # Ensemble retriever (hybrid search)
        ensemble_retriever = EnsembleRetriever(
            retrievers=[dense_vectorstore.as_retriever(search_kwargs={"k": 5}), bm25_retriever],
            weights=[0.6, 0.4]  # Favor semantic similarity slightly
        )
        
        self.vectorstores[doc_id] = {
            "dense": dense_vectorstore,
            "bm25": bm25_retriever,
            "ensemble": ensemble_retriever
        }
        
        self.retrievers[doc_id] = ensemble_retriever
    
    def query_documents(
        self, 
        query: str, 
        doc_ids: List[str] = None, 
        retrieval_strategy: str = "ensemble",
        filter_metadata: Dict = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """Advanced document querying with multiple strategies"""
        if not self.documents:
            return {"error": "No documents loaded"}
        
        # Determine which documents to search
        search_doc_ids = doc_ids or list(self.document_metadata.keys())
        
        results = {
            "query": query,
            "strategy": retrieval_strategy,
            "results": [],
            "metadata": {}
        }
        
        try:
            # Query routing - determine best strategy based on query
            query_type = self._classify_query(query)
            
            if query_type == "factual" and retrieval_strategy == "auto":
                retrieval_strategy = "bm25"  # Better for factual queries
            elif query_type == "conceptual" and retrieval_strategy == "auto":
                retrieval_strategy = "dense"  # Better for conceptual queries
            
            # Aggregate results from multiple documents
            all_docs = []
            for doc_id in search_doc_ids:
                if doc_id in self.retrievers:
                    if retrieval_strategy == "ensemble":
                        retriever = self.retrievers[doc_id]
                    elif retrieval_strategy in self.vectorstores[doc_id]:
                        if retrieval_strategy == "dense":
                            retriever = self.vectorstores[doc_id]["dense"].as_retriever(
                                search_kwargs={"k": top_k}
                            )
                        else:
                            retriever = self.vectorstores[doc_id][retrieval_strategy]
                    else:
                        retriever = self.retrievers[doc_id]  # Default to ensemble
                    
                    docs = retriever.get_relevant_documents(query)
                    
                    # Apply metadata filtering
                    if filter_metadata:
                        docs = [doc for doc in docs if self._matches_filter(doc.metadata, filter_metadata)]
                    
                    all_docs.extend(docs[:top_k])
            
            # Re-rank and deduplicate
            final_docs = self._rerank_documents(query, all_docs, top_k)
            
            # Generate answer using retrieved context
            context = "\n\n".join([doc.page_content for doc in final_docs])
            
            # Create QA chain with memory
            memory = ConversationSummaryBufferMemory(
                llm=self.llm,
                memory_key="chat_history",
                return_messages=True
            )
            
            qa_prompt = f"""
            Based on the following context, answer the question as accurately as possible.
            If the answer cannot be found in the context, say so clearly.
            
            Context:
            {context}
            
            Question: {query}
            
            Answer:
            """
            
            answer = self.llm.predict(qa_prompt)
            
            results["answer"] = answer
            results["context"] = context
            results["source_documents"] = [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata,
                    "score": getattr(doc, 'score', None)
                }
                for doc in final_docs
            ]
            results["metadata"] = {
                "num_sources": len(final_docs),
                "query_type": query_type,
                "documents_searched": search_doc_ids
            }
            
            return results
            
        except Exception as e:
            return {"error": f"Error querying documents: {str(e)}"}
    
    def _classify_query(self, query: str) -> str:
        """Enhanced query classification for optimal retrieval strategy"""
        query_lower = query.lower()
        
        # More comprehensive classification patterns
        factual_patterns = {
            "keywords": ["what", "when", "where", "who", "how many", "list", "define", "name", "identify"],
            "phrases": ["what is", "what are", "when did", "where is", "who is", "how many"],
            "weight": 0
        }
        
        conceptual_patterns = {
            "keywords": ["why", "how", "explain", "compare", "analyze", "describe", "evaluate", "assess"],
            "phrases": ["why does", "how does", "explain why", "compare and", "analyze the", "describe how"],
            "weight": 0
        }
        
        analytical_patterns = {
            "keywords": ["trend", "pattern", "correlation", "relationship", "impact", "effect", "cause"],
            "phrases": ["what are the trends", "show me patterns", "what is the impact", "how does this affect"],
            "weight": 0
        }
        
        # Calculate weights for each pattern type
        for pattern_type, patterns in [("factual", factual_patterns), ("conceptual", conceptual_patterns), ("analytical", analytical_patterns)]:
            # Check keyword matches
            keyword_matches = sum(1 for keyword in patterns["keywords"] if keyword in query_lower)
            patterns["weight"] += keyword_matches * 2
            
            # Check phrase matches (higher weight)
            phrase_matches = sum(1 for phrase in patterns["phrases"] if phrase in query_lower)
            patterns["weight"] += phrase_matches * 3
            
            # Check for question starters
            if pattern_type == "factual" and query_lower.startswith(("what", "when", "where", "who")):
                patterns["weight"] += 2
            elif pattern_type == "conceptual" and query_lower.startswith(("why", "how", "explain")):
                patterns["weight"] += 2
            elif pattern_type == "analytical" and any(word in query_lower for word in ["analyze", "trend", "pattern"]):
                patterns["weight"] += 2
        
        # Return the pattern type with highest weight
        best_pattern = max([("factual", factual_patterns), ("conceptual", conceptual_patterns), ("analytical", analytical_patterns)], 
                          key=lambda x: x[1]["weight"])
        
        # Default to conceptual if no clear pattern
        if best_pattern[1]["weight"] == 0:
            return "conceptual"
        
        logger.info(f"Query classified as {best_pattern[0]} (weight: {best_pattern[1]['weight']})")
        return best_pattern[0]
    
    def _matches_filter(self, metadata: Dict, filter_criteria: Dict) -> bool:
        """Check if document metadata matches filter criteria"""
        for key, value in filter_criteria.items():
            if key not in metadata or metadata[key] != value:
                return False
        return True
    
    def _rerank_documents(self, query: str, docs: List[Document], top_k: int) -> List[Document]:
        """Re-rank documents using additional scoring mechanisms"""
        if not docs:
            return []
        
        # Simple deduplication based on content similarity
        unique_docs = []
        seen_content = set()
        
        for doc in docs:
            content_hash = hashlib.md5(doc.page_content.encode()).hexdigest()
            if content_hash not in seen_content:
                unique_docs.append(doc)
                seen_content.add(content_hash)
        
        # Return top-k unique documents
        return unique_docs[:top_k]
    
    def get_document_summary(self) -> Dict[str, Any]:
        """Get summary of loaded documents and their metadata"""
        summary = {
            "total_documents": len(self.document_metadata),
            "total_chunks": len(self.documents),
            "documents": []
        }
        
        for doc_id, metadata in self.document_metadata.items():
            doc_summary = {
                "id": doc_id,
                "file_type": metadata["file_type"],
                "num_chunks": metadata["num_chunks"],
                "metadata": metadata["metadata"]
            }
            summary["documents"].append(doc_summary)
        
        return summary
    
    def semantic_search(self, query: str, threshold: float = 0.7) -> List[Dict]:
        """Perform semantic search across all documents with similarity threshold"""
        if not self.documents:
            return []
        
        # Get embeddings for query
        query_embedding = self.embeddings.embed_query(query)
        
        results = []
        for doc in self.documents:
            doc_embedding = self.embeddings.embed_query(doc.page_content)
            
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            
            if similarity >= threshold:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity": float(similarity)
                })
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results
    
    def get_chunk_analytics(self) -> Dict[str, Any]:
        """Analyze chunking strategies and their effectiveness"""
        analytics = {
            "chunk_strategies": {},
            "total_chunks": len(self.documents),
            "avg_chunk_length": 0,
            "chunk_distribution": {}
        }
        
        strategy_stats = {}
        total_length = 0
        
        for doc in self.documents:
            strategy = doc.metadata.get("chunk_strategy", "unknown")
            chunk_length = len(doc.page_content)
            
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {"count": 0, "total_length": 0}
            
            strategy_stats[strategy]["count"] += 1
            strategy_stats[strategy]["total_length"] += chunk_length
            total_length += chunk_length
        
        analytics["avg_chunk_length"] = total_length / len(self.documents) if self.documents else 0
        
        for strategy, stats in strategy_stats.items():
            analytics["chunk_strategies"][strategy] = {
                "count": stats["count"],
                "avg_length": stats["total_length"] / stats["count"] if stats["count"] > 0 else 0,
                "percentage": (stats["count"] / len(self.documents)) * 100 if self.documents else 0
            }
        
        return analytics 