from typing import TypedDict, List, Dict, Any
from langchain_core.documents import Document


class GraphState(TypedDict):
    """
    The central state object for the LangGraph workflow.
    This state is passed between nodes and updated as the workflow progresses.
    """
    question: str  # The user's original query
    documents: List[Document]  # Retrieved text chunks with metadata
    generation: str  # The LLM's final answer
    sources: List[Dict[str, Any]]  # List of source metadata [{"doc": "file.pdf", "page": 5}, ...]
