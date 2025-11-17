# System Architecture Diagram

## Data Flow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CEREVYN DOCUMENT INTELLIGENCE                   │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┐      ┌──────────────────────────────────┐
│      FRONTEND (React)        │      │     BACKEND (FastAPI)            │
│         Port 3000            │◄────►│        Port 8000                 │
└──────────────────────────────┘      └──────────────────────────────────┘
           │                                      │
           │                                      │
    ┌──────▼────────┐                    ┌───────▼────────┐
    │   App.jsx     │                    │   main.py      │
    │  (State Mgmt) │                    │  (API Routes)  │
    └───────┬───────┘                    └───────┬────────┘
            │                                     │
    ┌───────▼───────────────┐           ┌────────▼─────────┐
    │   Component Tree      │           │   LangGraph      │
    │                       │           │   Workflow       │
    │  ├─ Layout            │           │                  │
    │  ├─ FileUpload        │           │  Node 1:         │
    │  ├─ ChatWindow        │           │  retrieve_docs   │
    │  │  ├─ MessageList    │           │       ▼          │
    │  │  └─ Message        │           │  Node 2:         │
    │  └─ ChatInput         │           │  generate_answer │
    └───────────────────────┘           └────────┬─────────┘
                                                 │
                                        ┌────────▼─────────┐
                                        │   External APIs  │
                                        │                  │
                                        │  ├─ ChromaDB     │
                                        │  │  (Vectors)    │
                                        │  │               │
                                        │  └─ Groq API     │
                                        │     (LLM)        │
                                        └──────────────────┘
```

## Workflow 1: Document Upload

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐
│  User   │────►│FileUpload│────►│POST      │────►│PyMuPDF    │────►│ChromaDB  │
│ Selects │     │Component │     │/upload   │     │Loader     │     │Store     │
│  PDFs   │     │          │     │          │     │+ Chunking │     │          │
└─────────┘     └──────────┘     └──────────┘     └───────────┘     └──────────┘
                     ▲                                                     │
                     │                                                     │
                     └─────────────────Response──────────────────────────┘
                              "Processing complete"
```

## Workflow 2: Question Answering (RAG)

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌───────────┐
│  User   │────►│ChatInput │────►│POST      │────►│LangGraph  │
│  Types  │     │Component │     │/chat     │     │Invoke     │
│Question │     │          │     │          │     │           │
└─────────┘     └──────────┘     └──────────┘     └─────┬─────┘
                     ▲                                   │
                     │                                   ▼
                     │                          ┌────────────────┐
                     │                          │ retrieve_docs  │
                     │                          │ (Query Vector  │
                     │                          │  Database)     │
                     │                          └────────┬───────┘
                     │                                   │
                     │                                   ▼
                     │                          ┌────────────────┐
                     │                          │generate_answer │
                     │                          │ (Call Groq LLM)│
                     │                          └────────┬───────┘
                     │                                   │
                     └───────────────Response────────────┘
                       {"answer": "...", "sources": [...]}
```

## Component Communication

```
App.jsx State
    │
    ├─► chatHistory: Message[]
    ├─► isLoading: boolean
    ├─► fileUploadStatus: string
    └─► uploadMessage: string

Flows Down (Props) ▼
    │
    ├─► FileUpload
    │       └─► onUpload(), status, message
    │
    ├─► ChatWindow
    │       ├─► chatHistory, isLoading
    │       └─► MessageList
    │               └─► Message (for each message)
    │                       └─► role, content, sources
    │
    └─► ChatInput
            └─► onSendMessage(), disabled

Flows Up (Callbacks) ▲
    │
    ├─── handleFileUpload()
    └─── handleSendMessage()
```

## Backend Node Flow

```
GraphState: {
    question: string
    documents: Document[]
    generation: string
    sources: {doc, page}[]
}

Flow:
    1. Initial State
       ├─ question: "User's question"
       ├─ documents: []
       ├─ generation: ""
       └─ sources: []

    2. After retrieve_docs
       ├─ question: "User's question"
       ├─ documents: [Doc1, Doc2, ...]  ← Updated
       ├─ generation: ""
       └─ sources: [{doc, page}, ...]    ← Updated

    3. After generate_answer (Final)
       ├─ question: "User's question"
       ├─ documents: [Doc1, Doc2, ...]
       ├─ generation: "LLM answer"      ← Updated
       └─ sources: [{doc, page}, ...]
```

## File Processing Pipeline

```
PDF File
    │
    ▼
PyMuPDFLoader
    │ (Extracts text + metadata)
    │ Preserves: {source: "file.pdf", page: 5}
    ▼
RecursiveCharacterTextSplitter
    │ (Chunks: 1000 chars, overlap: 200)
    │ Preserves: metadata in each chunk
    ▼
Embedding Model
    │ (sentence-transformers/all-MiniLM-L6-v2)
    │ Converts text → vectors
    ▼
ChromaDB
    │ Stores: vectors + text + metadata
    └─► Ready for retrieval
```

## API Request/Response Formats

### Upload Endpoint
```
Request:
POST /upload
Content-Type: multipart/form-data
Body: FormData with 'files' field containing PDFs

Response:
{
    "status": "success",
    "files_processed": 2,
    "message": "Processed 2 file(s) into 45 chunks"
}
```

### Chat Endpoint
```
Request:
POST /chat
Content-Type: application/json
Body: {"question": "What is X?"}

Response:
{
    "answer": "X is defined as...",
    "sources": [
        {"doc": "document1.pdf", "page": 8},
        {"doc": "document2.pdf", "page": 3}
    ]
}
```

## Technology Stack Layers

```
┌────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                      │
│  React Components, CSS, Browser APIs                       │
└────────────────────────────────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│                   COMMUNICATION LAYER                      │
│  Axios, HTTP/REST, JSON, CORS                              │
└────────────────────────────────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                       │
│  FastAPI, Pydantic, LangGraph, Python                      │
└────────────────────────────────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC                        │
│  RAG Workflow, Document Processing, Retrieval              │
└────────────────────────────────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│                       DATA LAYER                           │
│  ChromaDB (Vectors), File System (PDFs)                    │
└────────────────────────────────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                       │
│  Groq API (LLM Inference), Embedding Models                │
└────────────────────────────────────────────────────────────┘
```
