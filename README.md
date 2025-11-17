# Cerevyn Document Intelligence

A full-stack RAG (Retrieval-Augmented Generation) application that allows users to upload PDF documents and ask questions about their content with precise source citations.

## Architecture

### Backend (FastAPI + LangGraph)
- **FastAPI**: RESTful API endpoints
- **LangGraph**: Orchestrates the RAG workflow
- **ChromaDB**: Vector storage for document embeddings
- **PyMuPDFLoader**: Extracts text with page metadata
- **Groq API**: Fast LLM inference for answer generation

### Frontend (React)
- **React 18**: Modern UI with hooks
- **Vite**: Fast development and build
- **Axios**: HTTP client for API calls
- **Component-based architecture**: Modular, maintainable code

## Features

✅ **Multi-file PDF Upload**: Process multiple documents simultaneously
✅ **Intelligent Text Chunking**: Preserves context with overlap
✅ **Vector Search**: Fast semantic retrieval with ChromaDB
✅ **Source Citations**: Every answer includes document name and page number
✅ **Real-time Chat**: Instant responses with loading indicators
✅ **Clean UI**: Professional, user-friendly interface

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API key ([Get one here](https://console.groq.com))

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

6. Start the backend server:
```bash
python main.py
```

Backend will be running at `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

Frontend will be running at `http://localhost:3000`

## Usage

1. **Upload Documents**: Use the sidebar to select and upload PDF files
2. **Wait for Processing**: Files are parsed, chunked, and embedded into the vector store
3. **Ask Questions**: Type your question in the chat input
4. **Review Sources**: Each answer includes citations to specific pages

## Workflow

### Document Ingestion
1. User uploads PDFs via React UI
2. Backend receives files via POST /upload
3. PyMuPDFLoader extracts text with page numbers
4. RecursiveCharacterTextSplitter chunks the text
5. Embeddings are generated and stored in ChromaDB

### Query & Generation (RAG)
1. User asks a question via React chat
2. Frontend sends POST /chat request
3. LangGraph executes workflow:
   - `retrieve_docs`: Queries ChromaDB for relevant chunks
   - `generate_answer`: Uses Groq LLM to generate answer
4. Backend returns answer with source citations
5. Frontend displays response with clickable sources

## Project Structure

```
Cerevyn Document Intelligence/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── graph_state.py          # LangGraph state definition
│   ├── graph_nodes.py          # RAG workflow nodes
│   ├── graph_workflow.py       # LangGraph workflow
│   ├── upload_handler.py       # PDF processing logic
│   ├── requirements.txt        # Python dependencies
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── api/               # API client
│   │   ├── App.jsx            # Main app component
│   │   └── main.jsx           # Entry point
│   ├── package.json
│   └── README.md
└── README.md                   # This file
```

## Technology Stack

**Backend:**
- FastAPI 0.104+
- LangChain & LangGraph
- ChromaDB 0.4+
- Groq Python SDK
- PyMuPDF

**Frontend:**
- React 18
- Vite 5
- Axios
- Modern CSS

## API Endpoints

### GET /
Health check endpoint

### POST /upload
Upload PDF documents
- **Input**: Multipart form data with PDF files
- **Output**: Processing status and chunk count

### POST /chat
Ask questions about documents
- **Input**: `{"question": "your question"}`
- **Output**: `{"answer": "...", "sources": [{"doc": "file.pdf", "page": 5}]}`

## Development Status

✅ Phase 1: Backend Architecture (LangGraph + FastAPI)
✅ Phase 2: API Endpoint Implementation
✅ Phase 3: Frontend Component Design
✅ Phase 4: Frontend-Backend Integration

## Contributing

This is a demonstration project showing best practices for RAG applications with precise citation tracking.

## License

MIT License
