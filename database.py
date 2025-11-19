import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient

# Environment variables are provided automatically in this environment
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]


def _with_timestamps(data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow()
    return {
        **data,
        "created_at": data.get("created_at", now),
        "updated_at": now,
    }


def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    collection = db[collection_name]
    doc = _with_timestamps(data)
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    collection = db[collection_name]
    cursor = collection.find(filter_dict or {}).limit(limit)
    docs: List[Dict[str, Any]] = []
    for d in cursor:
        d["_id"] = str(d.get("_id"))
        docs.append(d)
    return docs
