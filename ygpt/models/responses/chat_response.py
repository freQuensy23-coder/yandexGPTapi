from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str
    text: str


class GenerateTextChatResponse(BaseModel):
    """API response containing chat message.
    More info: https://cloud.yandex.ru/docs/yandexgpt/api-ref/TextGeneration/chat"""
    message: ChatMessage
    num_tokens: int
