import pydantic
from pydantic import BaseModel, Field


class GenerationOptions(BaseModel):
    """Generation options for Yandex GPT-3 model.
    :param partial_results: Return partial results or not.
    :param temperature: temperature is a parameter that controls the level of
      creativity and variability of the generated text. The higher the value,
      especially creative and variable text. The value lie
      in the range from 0 to 1. More info: https://discuss.huggingface.co/t/what-is-temperature/11924
    :param max_tokens: The maximum number of tokens to generate.
    """
    partialResults: bool # TODO
    temperature: float
    max_tokens: int

    @pydantic.field_validator("temperature")
    def temperature_validator(cls, v):
        if v < 0 or v > 1:
            raise ValueError("temperature must be between 0 and 1")
        return v

    @pydantic.field_validator("max_tokens")
    def max_tokens_validator(cls, v):
        if v < 1 or v > 7400:
            raise ValueError("max_tokens must be between 1 and 2048")
        return v
