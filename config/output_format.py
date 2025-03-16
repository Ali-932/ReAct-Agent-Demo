from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "react_agent_schema",
        "description": "Schema to follow for each step output",
        "strict": False,
        "schema": {
            "type": "object",
            "properties": {
                "iteration": {
                    "type": "integer",
                    "description": "Current step number in the reasoning process"
                },
                "observation": {
                    "type": "string",
                    "description": "Observation made from previous action or ability output"
                },
                "thought": {
                    "type": "string",
                    "description": "Agent's reasoning about the current situation and what to do next"
                },
                "confidence": {
                    "type": "number",
                    "description": "Confidence level in the current reasoning (0.0-1.0)"
                },
                "status": {
                    "type": "string",
                    "description": "Current status of task execution",
                    "enum": ["IN-PROGRESS", "FINISHED", "UNABLE TO PROCESS USER REQUEST"]
                },
            },
            "required": ["iteration", "observation", "thought", "status"],
            "additionalProperties": False
        }
    }
}


# Define types that match the JSON Schema using pydantic models
class Step(BaseModel):
    observation: str
    thought: str
    status: str
    iteration: int = 0
    timestamp: datetime = Field(default_factory=datetime.now)
    duration_ms: Optional[float] = None
    confidence: Optional[float] = None
