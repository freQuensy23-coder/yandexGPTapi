from typing import List

from pydantic import BaseModel


class Token(BaseModel):
    id: int
    text: str
    special: bool


class TokenizationResponse(BaseModel):
    tokens: List[Token]
