import PyPDF2
from typing import List
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFProcessor:
    def __init__(self, config: dict):
        """Initialize PDF processor with configuration"""
        
        self.input_path = config['pdf']['input_path']
        self.chunk_size = config['document']['chunk_size']
        self.chunk_overlap = config['document']['chunk_overlap']


    def process_pdf(self) -> List[str]:
        """Process PDF file and return chunks"""
        
        try:
            text = self._read_pdf()            
            chunks = self._create_chunks(text)
            
            logger.info(f"Successfully processed PDF into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise


    def _read_pdf(self) -> str:
        """Read PDF file and extract text"""
        
        try:
            with open(self.input_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            logger.error(f"Error reading PDF: {str(e)}")
            raise
        

    def _create_chunks(self, text: str) -> List[str]:
        """Split text into chunks"""
        
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                is_separator_regex=False,
            )
            chunks = text_splitter.split_text(text)
            return chunks
        except Exception as e:
            logger.error(f"Error creating chunks: {str(e)}")
            raise 