from langgraph.graph import StateGraph, END
from graph_state import GraphState
from graph_nodes import retrieve_docs, generate_answer


def create_rag_graph():
    """
    Create and compile the LangGraph workflow for RAG.
    
    The workflow follows this sequence:
    1. START -> retrieve_docs: Takes the user's question and retrieves relevant documents
    2. retrieve_docs -> generate_answer: Uses the retrieved documents to generate an answer
    3. generate_answer -> END: Returns the final state with the answer and sources
    
    Returns:
        Compiled LangGraph that can be invoked with an initial state
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(GraphState)
    
    # Add nodes to the graph
    workflow.add_node("retrieve_docs", retrieve_docs)
    workflow.add_node("generate_answer", generate_answer)
    
    # Define the edges (workflow sequence)
    workflow.set_entry_point("retrieve_docs")  # Start with document retrieval
    workflow.add_edge("retrieve_docs", "generate_answer")  # Then generate answer
    workflow.add_edge("generate_answer", END)  # Finally, end the workflow
    
    # Compile the graph
    app = workflow.compile()
    
    return app


# Create the compiled graph (singleton)
rag_graph = create_rag_graph()
