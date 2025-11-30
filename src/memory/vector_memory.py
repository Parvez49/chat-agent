"""
Memory management for agents using ChromaDB.
"""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from loguru import logger

from src.core import settings


class VectorMemory:
    """Vector-based memory using ChromaDB for semantic search."""
    
    def __init__(
        self,
        collection_name: str = "agent_memory",
        persist_directory: Optional[str] = None
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory or str(settings.data_dir / "chroma")
        
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            persist_directory=self.persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        
        logger.info(f"Initialized VectorMemory with collection: {collection_name}")
    
    def add(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None
    ):
        """Add a text entry to memory."""
        import uuid
        
        # Generate ID if not provided
        if not id:
            id = str(uuid.uuid4())
        
        # Generate embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        # Add to collection
        self.collection.add(
            ids=[id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}]
        )
        
        logger.debug(f"Added to memory: {id}")
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search memory for relevant entries."""
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        if results['ids']:
            for i, id in enumerate(results['ids'][0]):
                formatted_results.append({
                    "id": id,
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
        
        return formatted_results
    
    def delete(self, ids: List[str]):
        """Delete entries from memory by IDs."""
        self.collection.delete(ids=ids)
        logger.debug(f"Deleted {len(ids)} entries from memory")
    
    def clear(self):
        """Clear all entries from memory."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Cleared collection: {self.collection_name}")
    
    def get_count(self) -> int:
        """Get the number of entries in memory."""
        return self.collection.count()


class ConversationMemory:
    """Simple conversation buffer memory."""
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: List[Dict[str, str]] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.messages.append({
            "role": role,
            "content": content
        })
        
        # Maintain max size
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self, last_n: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation messages."""
        if last_n:
            return self.messages[-last_n:]
        return self.messages
    
    def clear(self):
        """Clear conversation history."""
        self.messages = []
    
    def get_context(self) -> str:
        """Get conversation as a single string."""
        return "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.messages
        ])


class HybridMemory:
    """Hybrid memory combining conversation buffer and vector search."""
    
    def __init__(
        self,
        collection_name: str = "agent_memory",
        max_conversation_messages: int = 20
    ):
        self.vector_memory = VectorMemory(collection_name)
        self.conversation_memory = ConversationMemory(max_conversation_messages)
    
    def add_interaction(
        self,
        user_message: str,
        assistant_message: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add a complete interaction to memory."""
        # Add to conversation buffer
        self.conversation_memory.add_message("user", user_message)
        self.conversation_memory.add_message("assistant", assistant_message)
        
        # Add to vector memory for long-term retrieval
        combined = f"User: {user_message}\nAssistant: {assistant_message}"
        self.vector_memory.add(combined, metadata)
    
    def get_relevant_context(
        self,
        query: str,
        top_k: int = 3,
        include_conversation: bool = True
    ) -> Dict[str, Any]:
        """Get relevant context from both memories."""
        context = {
            "conversation": [],
            "relevant_memories": []
        }
        
        # Get recent conversation
        if include_conversation:
            context["conversation"] = self.conversation_memory.get_messages()
        
        # Get relevant past memories
        context["relevant_memories"] = self.vector_memory.search(query, top_k)
        
        return context
    
    def clear(self):
        """Clear all memory."""
        self.conversation_memory.clear()
        self.vector_memory.clear()
