import ygpt.models.generation_options as generation_options
from ygpt.utils.string_template import StringTemplate

hostname_format_string = StringTemplate('https://llm.api.cloud.yandex.net/llm/{version}/{endpoint}')

ENDPOINTS = ['instruct', 'chat', 'embedding', 'tokenize']

default_generation_options = generation_options.GenerationOptions(
    partialResults=False,
    temperature=0.1,
    max_tokens=64)
