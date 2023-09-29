import models.generation_options
from ygpt.utils.string_template import StringTemplate

hostname_format_string = StringTemplate('https://llm.api.cloud.yandex.net/llm/{version}/{endpoint}')

ENDPOINTS = ['instruct', 'chat', 'embedding', 'tokenize']

default_generation_options = models.generation_options.GenerationOptions(
    max_tokens=64,
    temerature=0.2,
    partial_results=True
    )