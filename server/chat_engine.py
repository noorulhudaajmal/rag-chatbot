from openai import AzureOpenAI
import os
from typing import Dict, List
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatEngine:
    def __init__(self, config: Dict):
        """Initialize chat engine with Azure OpenAI client"""
        
        #Embeddings Model
        self.embedding_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_EMBEDDINGS_API_KEY"),
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDINGS_ENDPOINT")
        )
        
        # Chat Completion Model
        self.chat_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_CHAT_API_KEY"),
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
        )
        
        self.embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.temperature = config['azure']['temperature']
        self.max_tokens = config['azure']['max_tokens']
        self.system_prompt = config['azure']['system_prompt']


    def get_embeddings(self, text: str) -> List[float]:
        """Generate embeddings using Azure OpenAI"""
        try:
            response = self.embedding_client.embeddings.create(
                input=text,
                model=self.embedding_deployment
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise


    def generate_response(self, query: str, context: str) -> str:
        """Generate response using Azure OpenAI"""
        try:
            prompt = f"""
            Context:
            {context}

            User Query: {query}
            
            Instructions: Using the information from the "Context" section, answer the user's query. Be specific, accurate, and polite. If the context doesn't include relevant information, state that politely and offer alternative actions (e.g., "Please contact us directly for more details.").
            """

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            response = self.chat_client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
