from pydantic import BaseModel

class RecognitionResponse(BaseModel):
    text: str
    confidence: float = 0.0 