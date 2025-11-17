from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import shutil
from pathlib import Path
from models import ChatRequest, ChatResponse, SourceReference, UploadResponse
from graph_workflow import rag_graph
from upload_handler import process_pdf_upload
from graph_nodes import get_vectorstore

# Initialize FastAPI app
app = FastAPI(
    title="Cerevyn Document Intelligence API",
    description="Backend API for RAG-based document Q&A with citations",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded PDFs as static files
uploads_dir_path = Path("./uploads")
uploads_dir_path.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir_path)), name="uploads")


@app.on_event("startup")
async def startup_event():
    """Clean up ChromaDB and uploads on startup for fresh start."""
    print("🧹 Cleaning up previous data...")
    
    # Clear ChromaDB directory
    chroma_dir = Path("./chroma_db")
    if chroma_dir.exists():
        shutil.rmtree(chroma_dir)
        print(f"   ✓ Cleared ChromaDB directory: {chroma_dir}")
    
    # Clear uploads directory
    uploads_dir = Path("./uploads")
    if uploads_dir.exists():
        shutil.rmtree(uploads_dir)
        print(f"   ✓ Cleared uploads directory: {uploads_dir}")
    
    # Recreate directories
    chroma_dir.mkdir(exist_ok=True)
    uploads_dir.mkdir(exist_ok=True)
    
    print("✨ Database cleaned. Ready for fresh uploads!\n")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Cerevyn Document Intelligence API is running"}


@app.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload and process PDF documents.
    
    This endpoint:
    1. Receives multiple PDF files from the React frontend
    2. Saves them to disk temporarily
    3. Uses PyMuPDFLoader to extract text with page metadata
    4. Chunks the text using RecursiveCharacterTextSplitter
    5. Embeds the chunks and stores them in ChromaDB
    
    Args:
        files: List of uploaded PDF files
        
    Returns:
        UploadResponse with status and number of files processed
    """
    try:
        # Validate that files were uploaded
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Process the uploaded PDFs
        result = await process_pdf_upload(files)
        
        if not result["processed_files"]:
            raise HTTPException(
                status_code=400, 
                detail="No valid PDF files were processed"
            )
        
        return UploadResponse(
            status="success",
            files_processed=len(result["processed_files"]),
            message=f"Processed {len(result['processed_files'])} file(s) into {result['total_chunks']} chunks"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")


@app.get("/api/uploads")
async def list_uploaded_pdfs():
    """List uploaded PDF files with basic metadata and URLs."""
    try:
        files = []
        for entry in uploads_dir_path.glob("*.pdf"):
            stat = entry.stat()
            files.append({
                "name": entry.name,
                "size_bytes": stat.st_size,
                "modified_at": stat.st_mtime,
                "url": f"/uploads/{entry.name}",
            })
        # Sort by modified time desc
        files.sort(key=lambda f: f["modified_at"], reverse=True)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list uploads: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that processes user questions using RAG.
    
    Workflow:
    1. Receives the user's question
    2. Invokes the LangGraph workflow
    3. The graph retrieves relevant documents from ChromaDB
    4. The graph generates an answer using Groq LLM
    5. Returns the answer with source citations
    
    Args:
        request: ChatRequest containing the user's question
        
    Returns:
        ChatResponse with the generated answer and list of sources
    """
    # Initialize the graph state
    initial_state = {
        "question": request.question,
        "documents": [],
        "generation": "",
        "sources": []
    }
    
    # Invoke the LangGraph workflow
    final_state = rag_graph.invoke(initial_state)
    
    # Extract the answer and sources from the final state
    answer = final_state.get("generation", "I couldn't generate an answer.")
    sources_data = final_state.get("sources", [])
    
    # Convert sources to Pydantic models
    sources = [
        SourceReference(doc=src["doc"], page=src["page"])
        for src in sources_data
    ]
    
    return ChatResponse(answer=answer, sources=sources)


@app.delete("/api/uploads/{filename}")
async def delete_uploaded_pdf(filename: str):
    """Delete an uploaded PDF and its associated vectors from ChromaDB."""
    # basic filename sanitization
    if "/" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files can be deleted")

    file_path = uploads_dir_path / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Delete vectors for this file from ChromaDB
    try:
        vectorstore = get_vectorstore()
        collection = vectorstore._collection
        target_source = str(file_path)
        # Get ids of all chunks with this source
        matches = collection.get(where={"source": target_source}, include=["ids"])
        ids = matches.get("ids", []) if matches else []
        deleted_chunks = len(ids)
        if ids:
            collection.delete(ids=ids)
    except Exception as e:
        # Log but continue to delete file
        print(f"⚠️  Failed to delete vectors for {filename}: {e}")
        deleted_chunks = 0

    # Delete file from disk
    try:
        file_path.unlink()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {e}")

    return {"status": "success", "deleted_file": filename, "deleted_chunks": deleted_chunks}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
