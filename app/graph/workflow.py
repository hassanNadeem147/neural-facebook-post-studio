from app.graph.state import PostState
from app.graph.nodes.improved_post import improved_post_node
from app.graph.nodes.generate_post import generate_post_node
from langgraph.graph import StateGraph,START,END
from app.core.config import get_settings
settings = get_settings()
workflow = StateGraph(PostState)
workflow.add_node("generate_post",generate_post_node)
workflow.add_node("improved_post",improved_post_node)
workflow.add_edge(START,"generate_post")
workflow.add_edge("generate_post","improved_post")
workflow.add_edge("improved_post",END)
graph=workflow.compile()