from pydantic import BaseModel
from typing import Dict, Any

class GraphState(BaseModel):
    topic: str
    research_data: Dict[str, Any] = {}
    curriculum_draft: str | None = None
