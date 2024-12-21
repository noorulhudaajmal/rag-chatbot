import logging
from utils import load_config, initialize_system
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from chat_engine import ChatEngine
from retriever import Retriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_bot():
    """Initialize and setup the bot components"""
    try:
        #configuration
        config = load_config()
        
        retriever, chat_engine = initialize_system(config)
        return chat_engine, retriever
        
    except Exception as e:
        logger.error(f"Error setting up bot: {str(e)}")
        raise


def chat_loop(chat_engine: ChatEngine, retriever: Retriever):
    """Interactive chat loop"""
    
    print("\nWelcome to TechEase Solutions Assistant!")
    print("Type 'exit' to end the conversation\n")
    
    while True:
        try:
            # user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nThank you for using TechEase Solutions Assistant. Goodbye!")
                break
            
            if not user_input:
                continue
            
            context = retriever.get_relevant_context(user_input)            
            response = chat_engine.generate_response(user_input, context)
            
            print(f"\nAssistant: {response}\n")
            
        except Exception as e:
            logger.error(f"Error in chat loop: {str(e)}")
            print("\nI apologize, but I encountered an error. Please try again.")


def main():
    try:
        chat_engine, retriever = setup_bot()
        chat_loop(chat_engine, retriever)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        print("\nError initializing the system. Please check the logs for details.")



if __name__ == "__main__":
    main()