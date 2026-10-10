from app.graph.state import PostState
from langchain_groq import ChatGroq
from app.core.config import get_settings
from langchain_core.messages import SystemMessage
settings=get_settings()
llm=ChatGroq(groq_api_key=settings.GROQ_API_KEY.get_secret_value(), model_name=settings.GROQ_MODEL_NAME)
settings = get_settings()
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY.get_secret_value(),
    model=settings.GROQ_MODEL_NAME,
)
async def generate_post_node(state: PostState) -> PostState:
    """Creates a social media(Facebook) post from the user's request. It stores only the generated post text in the workflow state."""
    prompt = [
        SystemMessage(
            content=(
            "You are an expert Facebook content creator. Write one engaging "
            "Facebook post based on the user's request and conversation context.\n\n"
            "Follow these rules:\n"
            "- Return only the final post, without explanations or labels.\n"
            "- Use a friendly, conversational, and authentic tone.\n"
            "- Make the opening sentence attention-grabbing without using clickbait.\n"
            "- Write for a general Facebook audience using clear, natural language.\n"
            "- Keep the post concise and easy to read on mobile devices.\n"
            "- Use short paragraphs and line breaks when they improve readability.\n"
            "- Encourage natural engagement when appropriate, such as asking a relevant question.\n"
            "- Use emojis sparingly and only when they suit the topic and tone.\n"
            "- Use 2 to 4 relevant hashtags only when they add value.\n"
            "- Preserve important details from the user's request.\n"
            "- Do not invent facts, statistics, claims, or personal experiences.\n"
            "- Do not mention that you are an AI.\n"
            "- Do not use headings, quotation marks, or phrases such as 'Here is your post'."

            )
        ),
        *state["messages"],
    ]
    response = await llm.ainvoke(prompt)
    state["generated_post"] = response.content
    return state

