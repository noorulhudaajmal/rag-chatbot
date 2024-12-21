from typing import List, Tuple
import logging
from vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self, vector_store: VectorStore):
        """Initialize retriever with vector store"""
        self.vector_store = vector_store


    def get_relevant_context(self, query: str, k: int = 4) -> str:
        """Get relevant context for the query"""
        
        try:
            # similar chunks from vector store
            similar_chunks: List[Tuple[str, float]] = self.vector_store.similarity_search(query, k)            
            context = "\n\n".join([chunk[0] for chunk in similar_chunks])
            
            logger.info(f"Retrieved {len(similar_chunks)} relevant chunks for query")
            return context
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise