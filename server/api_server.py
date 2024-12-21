from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import load_config, initialize_system
import uvicorn
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#FastAPI app
app = FastAPI(title="RAG Chatbot API")

#  CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#rag system
config = load_config()
retriever, chat_engine = initialize_system(config)



class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    context: str = None



@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # context from the retriever
        context = retriever.get_relevant_context(request.message)
        
        #bot response
        response = chat_engine.generate_response(request.message, context)
        
        return ChatResponse(
            response=response,
            context=context
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}



static_path = os.path.join(os.path.dirname(__file__), "..", "web")
app.mount("/static", StaticFiles(directory=static_path), name="web")


@app.get("/")
async def serve_spa():
    return FileResponse(os.path.join(static_path, "index.html"))



if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True) 
    