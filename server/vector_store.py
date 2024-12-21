import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple
import logging
from chat_engine import ChatEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self, config: dict, chat_engine: ChatEngine):
        """Initialize vector store"""
        
        self.chat_engine = chat_engine
        self.index_path = os.path.join(config['vector_store']['index_path'], 'faiss_index')
        self.metadata_path = os.path.join(config['vector_store']['index_path'], 'metadata.pkl')
        self.dimension = config['vector_store']['dimension']
        
        if os.path.exists(self.index_path):
            self.load_index()
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.texts = []


    def add_texts(self, texts: List[str]):
        """Add texts to the vector store"""
        
        try:
            embeddings = []
            for text in texts:
                embedding = self.chat_engine.get_embeddings(text)
                embeddings.append(embedding)
            
            embeddings_array = np.array(embeddings).astype('float32')
            self.index.add(embeddings_array)
            self.texts.extend(texts)
            
            self.save_index()
            logger.info(f"Added {len(texts)} texts to vector store")
        except Exception as e:
            logger.error(f"Error adding texts to vector store: {str(e)}")
            raise


    def save_index(self):
        """Save the index and metadata"""
        try:
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            faiss.write_index(self.index, self.index_path)
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.texts, f)
            logger.info("Vector store saved successfully")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise


    def load_index(self):
        """Load the index and metadata"""
        try:
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.texts = pickle.load(f)
            logger.info("Vector store loaded successfully")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise


    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[str, float]]:
        """Search for similar texts"""
        try:
            query_embedding = self.chat_engine.get_embeddings(query)
            query_vector = np.array([query_embedding]).astype('float32')
            
            D, I = self.index.search(query_vector, k)
            
            results = []
            for i, (dist, idx) in enumerate(zip(D[0], I[0])):
                if idx < len(self.texts):
                    results.append((self.texts[idx], float(dist)))
            
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise 