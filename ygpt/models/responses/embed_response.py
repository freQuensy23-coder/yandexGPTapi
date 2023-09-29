import pydantic
from pydantic import BaseModel


class EmbeddingResponse(BaseModel):
    embedding: [float]
    num_tokens: int
