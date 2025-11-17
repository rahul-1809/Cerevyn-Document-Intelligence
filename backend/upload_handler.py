import os
import shutil
from pathlib import Path
from typing import List
from fastapi import UploadFile
from langchain_community.document_loaders import PyMuPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from graph_nodes import get_vectorstore, embedding_model

# Configure upload directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


async def process_pdf_upload(files: List[UploadFile]) -> dict:
    """
    Process uploaded PDF files and add them to the vector store.
    
    This function:
    1. Saves uploaded files to disk
    2. Uses PyMuPDFLoader to extract text with page numbers
    3. Chunks the text using RecursiveCharacterTextSplitter
    4. Embeds the chunks and stores them in ChromaDB with metadata
    
    Args:
        files: List of uploaded PDF files from FastAPI
        
    Returns:
        Dictionary with processing results
    """
    processed_files = []
    total_chunks = 0
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Characters per chunk
        chunk_overlap=200,  # Overlap to preserve context
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Get the vector store
    vectorstore = get_vectorstore()
    
    for file in files:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            print(f"   ⚠️  Skipping non-PDF file: {file.filename}")
            continue
            
        # Save the uploaded file
        file_path = UPLOAD_DIR / file.filename
        
        try:
            print(f"\n📄 Processing: {file.filename}")
            
            # Write file to disk
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"   ✓ Saved to: {file_path}")
            
            # Load PDF with PyMuPDFLoader (preserves page numbers)
            loader = PyMuPDFLoader(str(file_path))
            documents = loader.load()
            print(f"   ✓ Loaded {len(documents)} pages from PDF")
            
            # PyMuPDFLoader returns documents with metadata like:
            # {'source': 'path/to/file.pdf', 'page': 0, 'total_pages': 10}
            
            # Split documents into chunks
            # The splitter preserves the metadata from each document
            chunks = text_splitter.split_documents(documents)
            print(f"   ✓ Split into {len(chunks)} chunks")
            
            # Add chunks to vector store
            # ChromaDB will embed them and store with metadata
            vectorstore.add_documents(chunks)
            print(f"   ✓ Added {len(chunks)} chunks to ChromaDB")
            
            processed_files.append(file.filename)
            total_chunks += len(chunks)
            
        except Exception as e:
            print(f"Error processing {file.filename}: {str(e)}")
            # Continue processing other files
            continue
        
        finally:
            # Close the file
            file.file.close()
    
    return {
        "processed_files": processed_files,
        "total_chunks": total_chunks
    }


def clear_upload_directory():
    """Clear all files from the upload directory."""
    for file_path in UPLOAD_DIR.glob("*.pdf"):
        file_path.unlink()
