import yaml
import logging
from typing import Dict
import os

from chat_engine import ChatEngine
from pdf_processor import PDFProcessor
from retriever import Retriever
from vector_store import VectorStore


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> Dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        raise


def initialize_system(config: Dict):
    """Initialize system components"""
    try:
        
        chat_engine = ChatEngine(config)
        vector_store = VectorStore(config, chat_engine)
        
        doc_path = config['pdf']['input_path']        
        if not os.path.exists(doc_path):
            logger.error("Document missing.")
            return
        
        if not vector_store.texts:            
            os.makedirs(config['vector_store']['index_path'], exist_ok=True)
            logger.info("Processing PDF and creating vector store...")
            pdf_processor = PDFProcessor(config)
            chunks = pdf_processor.process_pdf()
            vector_store.add_texts(chunks)
            logger.info("Vector store created successfully")
        
        logger.info("System initialized successfully")
        
        #retriever
        retriever = Retriever(vector_store)
        
        return retriever, chat_engine
    
    except Exception as e:
        logger.error(f"Error initializing system: {str(e)}")
        raise 
    