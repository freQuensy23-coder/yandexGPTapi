from pydantic import BaseModel


class GeneratedTextInstruct(BaseModel):
    """Generated text alternative"""
    text: str
    score: float
    num_tokens: int


class GenerateTextInstructResponse(BaseModel):
    """Response containing generated text.
    More info https://cloud.yandex.ru/docs/yandexgpt/api-ref/TextGeneration/instruct"""
    alternatives: [GeneratedTextInstruct]
    num_prompt_tokens: int
