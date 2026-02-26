from pydantic import BaseModel
from typing import Optional
from typing_extensions import Literal

class RecruitAgentInput(BaseModel):
    """Input schema for RecruitAgent."""
    message: str
    email: str
    company: Optional[str]
    phone: Optional[str]
    notes: Optional[str] = "No additional notes"

class RecruitAgentOutput(BaseModel):
    """Output schema for RecruitAgent."""
    status: Literal["confirmed", "success", "rejected"]
    response: str
