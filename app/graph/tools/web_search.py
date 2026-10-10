from langchain_tavily import TavilySearch
from app.core.config import get_settings
settings = get_settings()
web_search_tool = TavilySearch(
    tavily_api_key=settings.TAVILY_API_KEY.get_secret_value(),
    max_results=3,
    search_depth="basic",
    include_answer=False,
    include_raw_content=False,
)
