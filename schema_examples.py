from pydantic import BaseModel, Field
from typing import List, Optional

# Examples of other potential schemas for inspiration / extension

class AgentAction(BaseModel):
    agent: str  # frontend, backend, data, testing, integration, devops
    action: str  # plan, codegen, review, test, integrate, deploy
    detail: str
    status: str  # queued, running, passed, failed


class BuildArtifact(BaseModel):
    name: str
    type: str  # bundle, wheel, container
    size_kb: int
    checksum: str


class TestResult(BaseModel):
    name: str
    passed: bool
    duration_ms: int
    coverage_percent: float
