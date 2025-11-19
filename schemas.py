from pydantic import BaseModel, Field
from typing import List, Optional

# Each Pydantic model maps to a Mongo collection with lowercased class name

class UserStory(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    acceptance_criteria: List[str] = []
    sprint: Optional[str] = None
    priority: Optional[str] = Field(default="Medium", pattern="^(Low|Medium|High|Critical)$")
    tags: List[str] = []


class PipelineEvent(BaseModel):
    stage: str
    status: str
    message: str
    timestamp: str


class ProjectReport(BaseModel):
    overview: str
    metrics: dict
    events: List[PipelineEvent]
