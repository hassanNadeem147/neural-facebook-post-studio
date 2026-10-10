from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Annotated, List, NotRequired, TypedDict
class PostState(TypedDict):
    """The messages and post versions managed by the workflow."""
    messages: Annotated[List[BaseMessage], add_messages]
    generated_post: NotRequired[str]
    improved_post: NotRequired[str]


    