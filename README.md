# RAG-Powered Chatbot for Business Services Info

This project demonstrates a Retrieval-Augmented Generation (RAG) chatbot integrated into a company's website. The chatbot interacts with users, providing detailed and accurate responses based on business services information.

#### Project Objective
This project was created as part of my portfolio to demonstrate expertise in building a modern RAG system for real-world applications.


## Features

- **RAG Chatbot**: retrieves business information and provides intelligent responses to user queries.
- **Real-Time Query Handling**: Cosine similarity-based vector search for information retrieval.
- **Embeddings and LLM**: Powered by text-embeddings-3-small and GPT-3.5-turbo models.

## How It Works

### Document Preparation
1. Business services information document ingestion
2. Document splitting into manageable chunks (1000 tokens/chunk, 200-token overlap)

### Database Creation
- Chunked data storage in Faiss db.
- Vector embeddings generation using text-embeddings-3-small embeddings model.

### Chatbot Flow
1. **User Query**
2. **Query Matching**: 
   - Query vectorization
   - Top 4 relevant chunks retrieval using cosine similarity
3. **Prompt Generation**: Formatting retrieved chunks and query
4. **Response Generation**: Use of ChatGPT-3.5-turbo

## Technologies Used

- Faissdb: Vectorized data storage and querying
- OpenAI API: text-embeddings-3-small and ChatGPT-3.5-turbo models
- FastAPI: API endpoint handling

## Setup and Installation

### Prerequisites
- Python 3.9 or later
- OpenAI API key

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/noorulhudaajmal/rag-chatbot.git
   cd rag-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file and openai api keys.

4. **Run the FastAPI server**
   ```bash
   uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
   ```


## Demo 
![/demo-video](./demo/run.mp4)