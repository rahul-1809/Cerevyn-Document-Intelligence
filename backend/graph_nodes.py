import os
from dotenv import load_dotenv
from groq import Groq
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from graph_state import GraphState
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize embedding model (using a fast, local model)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ChromaDB configuration
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = "document_intelligence"


def get_vectorstore():
    """Get or create the ChromaDB vector store."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=CHROMA_PERSIST_DIR
    )


def retrieve_docs(state: GraphState) -> Dict[str, Any]:
    """
    Node 1: Retrieve relevant document chunks from ChromaDB.
    
    This node:
    1. Takes the question from the state
    2. Embeds the question using the embedding model
    3. Queries ChromaDB to find the most similar document chunks
    4. Extracts the retrieved documents and their metadata (page numbers, source files)
    5. Updates the state with the documents and sources
    
    Args:
        state: The current graph state containing the user's question
        
    Returns:
        Dictionary with updated 'documents' and 'sources' fields
    """
    question = state["question"]
    print(f"\n🔍 Retrieving documents for question: '{question}'")
    
    # Get the vector store
    vectorstore = get_vectorstore()
    
    # Check if collection has documents
    try:
        collection = vectorstore._collection
        count = collection.count()
        print(f"   📊 ChromaDB collection has {count} document chunks")
        
        if count == 0:
            print("   ⚠️  No documents in database! Please upload PDFs first.")
            return {
                "documents": [],
                "sources": []
            }
    except Exception as e:
        print(f"   ⚠️  Error checking collection: {e}")
    
    # Retrieve the top-k most relevant documents with scores
    try:
        results = vectorstore.similarity_search_with_score(
            question,
            k=10  # Get more candidates for filtering
        )
        
        # Filter by relevance score (lower is better for L2 distance)
        # Keep only documents with good similarity scores
        RELEVANCE_THRESHOLD = 1.0  # Adjust based on your needs (0.5-1.5 typical range)
        
        retrieved_docs = []
        for doc, score in results:
            if score <= RELEVANCE_THRESHOLD:
                retrieved_docs.append(doc)
                print(f"   📄 Score: {score:.3f} - {os.path.basename(doc.metadata.get('source', 'unknown'))}, Page {doc.metadata.get('page', 0)}")
        
        # Limit to top 5 most relevant
        retrieved_docs = retrieved_docs[:5]
        
        if not retrieved_docs:
            print(f"   ⚠️  No documents above relevance threshold ({RELEVANCE_THRESHOLD})")
            # Fall back to top results without filtering
            retrieved_docs = [doc for doc, _ in results[:5]]
        
        print(f"   ✓ Using {len(retrieved_docs)} highly relevant document chunks")
    except Exception as e:
        print(f"   ❌ Error during retrieval: {e}")
        return {
            "documents": [],
            "sources": []
        }
    
    # Extract sources from metadata
    sources = []
    seen_sources = set()  # To avoid duplicate source references
    
    for doc in retrieved_docs:
        # Extract metadata
        source_file = doc.metadata.get("source", "unknown")
        page_num = doc.metadata.get("page", 0)
        
        # Create a unique identifier for this source
        source_key = f"{source_file}:{page_num}"
        
        if source_key not in seen_sources:
            sources.append({
                "doc": os.path.basename(source_file),  # Just the filename, not full path
                "page": page_num
            })
            seen_sources.add(source_key)
    
    print(f"   ✓ Extracted {len(sources)} unique sources\n")
    
    return {
        "documents": retrieved_docs,
        "sources": sources
    }


def generate_answer(state: GraphState) -> Dict[str, Any]:
    """
    Node 2: Generate an answer using the Groq LLM.
    
    This node:
    1. Takes the question and retrieved documents from the state
    2. Formats them into a clear prompt for the LLM
    3. Calls the Groq API to generate an answer
    4. Updates the state with the generated answer
    
    Args:
        state: The current graph state containing the question and retrieved documents
        
    Returns:
        Dictionary with updated 'generation' field
    """
    question = state["question"]
    documents = state["documents"]
    
    print(f"🤖 Generating answer for: '{question}'")
    print(f"   📚 Using {len(documents)} document chunks")
    
    # Handle case where no documents were retrieved
    if not documents:
        print("   ⚠️  No documents available for context!")
        return {
            "generation": "I don't have any documents to answer from. Please upload PDF files first."
        }
    
    # Format the context from retrieved documents
    context = "\n\n".join([
        f"[Document: {doc.metadata.get('source', 'unknown')}, Page: {doc.metadata.get('page', 0)}]\n{doc.page_content}"
        for doc in documents
    ])
    
    # Create the prompt
    prompt = f"""You are a helpful AI assistant that answers questions based strictly on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Answer the question using ONLY the information from the context above
- Be concise and accurate
- If the context doesn't contain enough information to answer the question, say so
- Do not make up information or use external knowledge

Answer:"""
    
    # Determine model (updated; previous model deprecated). Allow override via env var.
    groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    print(f"   🚀 Calling Groq API with model: {groq_model}")
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=groq_model,
            temperature=0.2,
            max_tokens=768
        )
        answer = chat_completion.choices[0].message.content
        print(f"   ✓ Generated answer (length: {len(answer)} chars)\n")
    except Exception as e:
        print(f"   ❌ Groq API error: {e}\n")
        answer = f"I encountered an error while generating the answer: {str(e)}"
    
    return {
        "generation": answer
    }
