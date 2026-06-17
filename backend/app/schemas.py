from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class Source(BaseModel):
    title: str
    snippet: str
    score: float


class TimelineStep(BaseModel):
    step: str
    status: str
    detail: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    steps: list[TimelineStep]
    project_type: str
