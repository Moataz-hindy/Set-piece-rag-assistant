from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    vision_context: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
