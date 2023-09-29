import pydantic
from pydantic import BaseModel
from typing import List


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    num_tokens: int
