"""
Enterprise Vector Database Persistence Layer
=============================================
Demonstrates production-ready vector storage with:
- Persistent vector storage
- Index optimization
- Backup and recovery
- Performance monitoring
"""

import os
import pickle
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from pathlib import Path
import logging
import shutil
import threading
import time

logger = logging.getLogger(__name__)

class VectorDatabaseManager:
    """Production-ready vector database with persistence and optimization"""
    
    def __init__(self, db_path: str = "vector_db", backup_interval: int = 3600):
        self.db_path = Path(db_path)
        self.backup_interval = backup_interval
        self.db_path.mkdir(exist_ok=True)
        
        # Initialize storage
        self.vectors_file = self.db_path / "vectors.npy"
        self.metadata_file = self.db_path / "metadata.json"
        self.index_file = self.db_path / "index.pkl"
        
        # Load existing data
        self.vectors = self._load_vectors()
        self.metadata = self._load_metadata()
        self.index = self._load_index()
        
        # Performance metrics
        self.metrics = {
            "total_vectors": len(self.vectors),
            "queries_served": 0,
            "avg_query_time": 0.0,
            "cache_hits": 0
        }
        
        # Start background processes
        self._start_backup_thread()
        
        logger.info(f"VectorDatabaseManager initialized with {len(self.vectors)} vectors")
    
    def _load_vectors(self) -> np.ndarray:
        """Load vectors from persistent storage"""
        if self.vectors_file.exists():
            return np.load(self.vectors_file)
        return np.empty((0, 384))  # Default dimension for all-MiniLM-L6-v2
    
    def _load_metadata(self) -> List[Dict]:
        """Load metadata from persistent storage"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return []
    
    def _load_index(self) -> Optional[Any]:
        """Load FAISS index from persistent storage"""
        if self.index_file.exists():
            with open(self.index_file, 'rb') as f:
                return pickle.load(f)
        return None
    
    def add_vectors(self, vectors: np.ndarray, metadata: List[Dict]) -> None:
        """Add vectors with metadata to the database"""
        if len(vectors) != len(metadata):
            raise ValueError("Vectors and metadata must have same length")
        
        # Append to existing vectors
        if len(self.vectors) == 0:
            self.vectors = vectors
        else:
            self.vectors = np.vstack([self.vectors, vectors])
        
        # Append metadata
        self.metadata.extend(metadata)
        
        # Update metrics
        self.metrics["total_vectors"] = len(self.vectors)
        
        # Rebuild index if needed
        self._rebuild_index()
        
        # Persist changes
        self._persist_data()
        
        logger.info(f"Added {len(vectors)} vectors to database")
    
    def _rebuild_index(self) -> None:
        """Rebuild FAISS index for efficient similarity search"""
        try:
            import faiss
            
            if len(self.vectors) > 0:
                dimension = self.vectors.shape[1]
                self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
                
                # Normalize vectors for cosine similarity
                normalized_vectors = self.vectors / np.linalg.norm(self.vectors, axis=1, keepdims=True)
                self.index.add(normalized_vectors.astype('float32'))
                
                logger.info(f"Rebuilt FAISS index with {len(self.vectors)} vectors")
        except ImportError:
            logger.warning("FAISS not available, using numpy-based similarity search")
            self.index = None
    
    def similarity_search(self, query_vector: np.ndarray, top_k: int = 5, threshold: float = 0.5) -> List[Dict]:
        """Perform similarity search with optional threshold filtering"""
        start_time = time.time()
        
        if len(self.vectors) == 0:
            return []
        
        # Normalize query vector
        query_norm = query_vector / np.linalg.norm(query_vector)
        
        if self.index is not None:
            # Use FAISS for efficient search
            scores, indices = self.index.search(query_norm.reshape(1, -1).astype('float32'), top_k)
            results = []
            
            for score, idx in zip(scores[0], indices[0]):
                if score >= threshold:
                    results.append({
                        "score": float(score),
                        "metadata": self.metadata[idx],
                        "vector_id": int(idx)
                    })
        else:
            # Fallback to numpy-based search
            normalized_vectors = self.vectors / np.linalg.norm(self.vectors, axis=1, keepdims=True)
            similarities = np.dot(normalized_vectors, query_norm)
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                score = similarities[idx]
                if score >= threshold:
                    results.append({
                        "score": float(score),
                        "metadata": self.metadata[idx],
                        "vector_id": int(idx)
                    })
        
        # Update metrics
        query_time = time.time() - start_time
        self.metrics["queries_served"] += 1
        self.metrics["avg_query_time"] = (
            (self.metrics["avg_query_time"] * (self.metrics["queries_served"] - 1) + query_time) /
            self.metrics["queries_served"]
        )
        
        logger.debug(f"Similarity search completed in {query_time:.3f}s, found {len(results)} results")
        return results
    
    def _persist_data(self) -> None:
        """Persist vectors, metadata, and index to disk"""
        try:
            # Save vectors
            np.save(self.vectors_file, self.vectors)
            
            # Save metadata
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            # Save index
            if self.index is not None:
                with open(self.index_file, 'wb') as f:
                    pickle.dump(self.index, f)
            
            logger.debug("Data persisted successfully")
        except Exception as e:
            logger.error(f"Failed to persist data: {e}")
    
    def _start_backup_thread(self) -> None:
        """Start background thread for periodic backups"""
        def backup_worker():
            while True:
                time.sleep(self.backup_interval)
                self.create_backup()
        
        backup_thread = threading.Thread(target=backup_worker, daemon=True)
        backup_thread.start()
        logger.info("Backup thread started")
    
    def create_backup(self) -> str:
        """Create a timestamped backup of the database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.db_path.parent / f"backup_{timestamp}"
        
        try:
            shutil.copytree(self.db_path, backup_dir)
            logger.info(f"Backup created: {backup_dir}")
            return str(backup_dir)
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return ""
    
    def restore_backup(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            backup_dir = Path(backup_path)
            if not backup_dir.exists():
                logger.error(f"Backup directory not found: {backup_path}")
                return False
            
            # Remove current data
            if self.db_path.exists():
                shutil.rmtree(self.db_path)
            
            # Restore from backup
            shutil.copytree(backup_dir, self.db_path)
            
            # Reload data
            self.vectors = self._load_vectors()
            self.metadata = self._load_metadata()
            self.index = self._load_index()
            
            logger.info(f"Database restored from backup: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
    
    def optimize_database(self) -> Dict[str, Any]:
        """Optimize database performance"""
        start_time = time.time()
        
        optimization_results = {
            "vectors_before": len(self.vectors),
            "metadata_before": len(self.metadata),
            "duplicates_removed": 0,
            "index_rebuilt": False,
            "optimization_time": 0.0
        }
        
        # Remove duplicate vectors
        if len(self.vectors) > 0:
            unique_indices = []
            seen_hashes = set()
            
            for i, vector in enumerate(self.vectors):
                vector_hash = hash(vector.tobytes())
                if vector_hash not in seen_hashes:
                    seen_hashes.add(vector_hash)
                    unique_indices.append(i)
            
            duplicates_removed = len(self.vectors) - len(unique_indices)
            
            if duplicates_removed > 0:
                self.vectors = self.vectors[unique_indices]
                self.metadata = [self.metadata[i] for i in unique_indices]
                optimization_results["duplicates_removed"] = duplicates_removed
                
                # Rebuild index
                self._rebuild_index()
                optimization_results["index_rebuilt"] = True
                
                # Persist optimized data
                self._persist_data()
        
        optimization_results["vectors_after"] = len(self.vectors)
        optimization_results["metadata_after"] = len(self.metadata)
        optimization_results["optimization_time"] = time.time() - start_time
        
        logger.info(f"Database optimization completed: {optimization_results}")
        return optimization_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        stats = {
            "database_stats": {
                "total_vectors": len(self.vectors),
                "vector_dimension": self.vectors.shape[1] if len(self.vectors) > 0 else 0,
                "metadata_entries": len(self.metadata),
                "index_available": self.index is not None,
                "database_size_mb": self._get_database_size_mb()
            },
            "performance_metrics": self.metrics.copy(),
            "recent_activity": {
                "last_backup": self._get_last_backup_time(),
                "uptime_hours": self._get_uptime_hours()
            }
        }
        
        return stats
    
    def _get_database_size_mb(self) -> float:
        """Calculate total database size in MB"""
        total_size = 0
        for file_path in self.db_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size / (1024 * 1024)  # Convert to MB
    
    def _get_last_backup_time(self) -> Optional[str]:
        """Get timestamp of last backup"""
        backup_dirs = [d for d in self.db_path.parent.glob("backup_*") if d.is_dir()]
        if backup_dirs:
            latest_backup = max(backup_dirs, key=lambda x: x.stat().st_mtime)
            return datetime.fromtimestamp(latest_backup.stat().st_mtime).isoformat()
        return None
    
    def _get_uptime_hours(self) -> float:
        """Calculate uptime in hours"""
        # This is a simplified calculation - in production, you'd track actual start time
        return time.time() / 3600  # Placeholder implementation
    
    def close(self) -> None:
        """Clean shutdown of the database"""
        self._persist_data()
        logger.info("Vector database closed successfully") 