# Cerevyn Document Intelligence - Backend

This is the backend API for the Cerevyn Document Intelligence application, built with FastAPI and LangGraph.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Add your Groq API key to the `.env` file:
```
GROQ_API_KEY=your_actual_api_key_here
```

## Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Architecture

### Core Components

- **models.py**: Pydantic models for API requests/responses
- **graph_state.py**: LangGraph state definition (TypedDict)
- **graph_nodes.py**: Node functions for the RAG workflow
  - `retrieve_docs`: Queries ChromaDB for relevant documents
  - `generate_answer`: Uses Groq LLM to generate answers
- **graph_workflow.py**: LangGraph workflow definition with edges
- **main.py**: FastAPI application with endpoints

### Workflow

1. User sends question to `/chat` endpoint
2. LangGraph executes: retrieve_docs → generate_answer
3. Response includes answer + source citations (doc name, page number)

## API Endpoints

### POST /upload
Upload PDF documents to the knowledge base.

**Request**: Multipart form data with PDF files
**Response**: 
```json
{
  "status": "success",
  "files_processed": 2,
  "message": "Processed 2 file(s) into 45 chunks"
}
```

### POST /chat
Send a question and receive an answer with source citations.

**Request**:
```json
{
  "question": "What is the Component-Based Approach?"
}
```

**Response**:
```json
{
  "answer": "The Component-Based Approach is...",
  "sources": [
    {"doc": "tech_spec.pdf", "page": 8},
    {"doc": "architecture.pdf", "page": 3}
  ]
}
```

## Project Status

✅ Phase 1: Backend Architecture (LangGraph + FastAPI)
✅ Phase 2: API Endpoints (/upload, /chat with CORS)
✅ Phase 3: Frontend Components (React)
✅ Phase 4: Frontend-Backend Integration

**Note**: Import errors are expected until dependencies are installed. Run `pip install -r requirements.txt` to resolve.

---

## Additional Endpoints and Static Files

- `GET /api/uploads`: List uploaded PDFs with basic metadata and their URLs (served under `/uploads/{filename}` for in-app viewing)
- `DELETE /api/uploads/{filename}`: Delete an uploaded PDF and remove its corresponding vector chunks from ChromaDB
- Static PDFs: `GET /uploads/{filename}`

Example delete:
```bash
curl -X DELETE http://localhost:8000/api/uploads/AI___ML_Resume.pdf
```

## Run Tips

```bash
source venv/bin/activate
export GROQ_MODEL=llama-3.1-8b-instant
export TOKENIZERS_PARALLELISM=false
python main.py
```

## Behavior and Notes

- On startup, the app clears `./chroma_db` and `./uploads` to ensure a clean state
- Retrieval uses similarity scores with a relevance threshold to filter weak matches
- CORS allows React dev servers at `http://localhost:3000` and `http://localhost:5173`
