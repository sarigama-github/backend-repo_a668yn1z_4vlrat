from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import UserStory, PipelineEvent, ProjectReport

app = FastAPI(title="Collaborative Agentic Platform API", version="0.1.0")

# CORS for frontend preview
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "CAP Backend is running", "version": app.version}


@app.get("/test")
def test_db():
    try:
        collections = db.list_collection_names()
        return {
            "backend": "fastapi",
            "database": "mongodb",
            "database_url": "hidden",
            "database_name": db.name,
            "connection_status": "ok",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "fastapi", "database": "mongodb", "connection_status": f"error: {e}"}


class UploadPayload(BaseModel):
    source: str  # 'ado' or 'manual'
    items: List[UserStory]


@app.post("/stories/import")
def import_stories(payload: UploadPayload):
    inserted_ids: List[str] = []
    for story in payload.items:
        data = story.model_dump()
        inserted_id = create_document("userstory", data)
        inserted_ids.append(inserted_id)
    return {"inserted": len(inserted_ids), "ids": inserted_ids}


@app.get("/stories")
def list_stories(limit: int = 50):
    stories = get_documents("userstory", limit=limit)
    return {"count": len(stories), "items": stories}


# Simulated Azure DevOps pipeline events with authentic sequence and fields
STAGES = [
    "Requirement Extraction",
    "Task Assignment",
    "Code Generation",
    "Static Analysis & Security",
    "Unit Testing",
    "Integration",
    "Build",
    "Deploy",
]


@app.get("/pipeline/start")
def start_pipeline(project: Optional[str] = None):
    now = datetime.utcnow()
    events: List[PipelineEvent] = []

    def ev(stage: str, status: str, message: str):
        return PipelineEvent(stage=stage, status=status, message=message, timestamp=now.isoformat() + "Z")

    # We simulate an authentic flow; frontend animates these progressively
    events.append(ev("Requirement Extraction", "running", "Fetching user stories from ADO and uploaded sources"))
    events.append(ev("Task Assignment", "queued", "Assigning tasks to specialized agents"))
    events.append(ev("Code Generation", "queued", "Generating code for services and UI"))
    events.append(ev("Static Analysis & Security", "queued", "Running linters, SAST, license checks"))
    events.append(ev("Unit Testing", "queued", "Executing unit tests with coverage"))
    events.append(ev("Integration", "queued", "Merging branches and validating contracts"))
    events.append(ev("Build", "queued", "Bundling artifacts and producing images"))
    events.append(ev("Deploy", "queued", "Promoting to staging environment"))

    return {"project": project or "demo", "events": [e.model_dump() for e in events]}


@app.get("/metrics")
def metrics():
    # Simulated but coherent metrics with real-world fields
    data = {
        "time_saved_percent": 48.6,
        "manual_tasks_automated": 132,
        "testing_throughput": 324,  # test cases/hour
        "security_status": "Compliant",
        "coverage_percent": 82.4,
        "build_success_rate": 96.3,
        "mttr_minutes": 12.5,
    }
    return data


@app.get("/report")
def report():
    events = [
        {"stage": "Requirement Extraction", "status": "passed", "message": "Parsed 18 stories", "timestamp": datetime.utcnow().isoformat() + "Z"},
        {"stage": "Task Assignment", "status": "passed", "message": "Assigned to 6 agents", "timestamp": datetime.utcnow().isoformat() + "Z"},
        {"stage": "Code Generation", "status": "passed", "message": "Generated 43 files", "timestamp": datetime.utcnow().isoformat() + "Z"},
        {"stage": "Testing", "status": "passed", "message": "312 tests executed, 2 quarantined", "timestamp": datetime.utcnow().isoformat() + "Z"},
        {"stage": "Integration", "status": "passed", "message": "All checks green on PR #102", "timestamp": datetime.utcnow().isoformat() + "Z"},
    ]
    metrics_data = {
        "time_saved_percent": 48.6,
        "manual_tasks_automated": 132,
        "coverage_percent": 82.4,
        "build_success_rate": 96.3,
    }
    pr = ProjectReport(overview="CAP simulated project report", metrics=metrics_data, events=[PipelineEvent(**e) for e in events])
    return pr
