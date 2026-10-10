from pathlib import Path

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.model_schema import UserRequestQuery, UserRequestResponse
from app.graph.workflow import graph
from app.core.config import get_settings  # 👈 Import settings to auto-trigger LangSmith config
from langchain_core.messages import HumanMessage
# Initialize configuration (automatically exports LangSmith variables to os.environ)
settings = get_settings()
app = FastAPI(title="Facebook Post Generator")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


@app.get("/", response_class=FileResponse)
async def home():
    return FileResponse(
        Path(__file__).resolve().parent.parent / "frontend" / "index.html"
    )


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {
        "message": "healthy",
        "status_code": status.HTTP_200_OK
    }
@app.post("/query", response_model=UserRequestResponse)
async def query_post(request: UserRequestQuery):  # 👈 FIX: Changed from UserRequestResponse to UserRequestQuer
    # sourcery skip: raise-from-previous-error, reintroduce-else, swap-if-else-branches, use-named-expressiony
    """Generates an improved Facebook post from the user's request. 
    It returns the original query and the final improved post content.
    """
    try:
        # Pass a run_name and tags to LangSmith to track individual API calls cleanly
        langsmith_config = {
            "configurable": {"run_name": "FastAPI_FB_Post_Generation"},
            "tags": ["production", "api-endpoint"]
        }
        
        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=request.query)]}, # 👈 Graph state expects a list of messages
            config=langsmith_config
        )
    except Exception as e:
        # Log the exception 'e' internally here if you use a logger
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process the post request due to an internal workflow error."
        )
    improved_post = result.get("improved_post")
    if not improved_post:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The workflow completed but did not generate an improved post.",
        )
    # Return matching fields required by UserRequestResponse schema
    return UserRequestResponse(
        query=request.query, 
        improved_post=improved_post
    )


app.mount(
    "/frontend",
    StaticFiles(directory=Path(__file__).resolve().parent.parent / "frontend", html=True),
    name="frontend",
)
