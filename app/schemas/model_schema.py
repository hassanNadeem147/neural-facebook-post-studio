from pydantic import BaseModel,Field

class UserRequestQuery(BaseModel):
    query:str = Field(
        ...,
        min_length=2,
        max_length=250
    )
class UserRequestResponse(BaseModel):
    query:str
    improved_post: str = Field(
    ...,
    description="The improved Facebook post.",
    )