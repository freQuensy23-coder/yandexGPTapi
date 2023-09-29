from ygpt import config
from ygpt.rest_adapter import RestAdapter
from ygpt.models.responses.embed_response import EmbeddingResponse
from ygpt.models.responses.chat_response import GenerateTextChatResponse
from ygpt.models.responses.instruct_response import GenerateTextInstructResponse
from ygpt.models.responses.tokenize_response import TokenizationResponse
from ygpt.models.generation_options import GenerationOptions


class YandexGPT(RestAdapter):
    def embed(self, text: str,
              embedding_type: str,
              model: str = 'general:embedding')-> EmbeddingResponse:
        """Generate an embedding for the input text.
        Args:
            embedding_type (str): The type of embedding to generate. Options are:
                - EMBEDDING_TYPE_UNSPECIFIED: Unspecified embedding type.
                - EMBEDDING_TYPE_QUERY: Embedding for a short query.
                - EMBEDDING_TYPE_DOCUMENT: Embedding for a longer document.
            model (str): The name of the model to use for embedding.
                Currently only 'general:embedding' is supported.
            text (str): The input text to generate an embedding for.

        Returns:
            embedding: The embedding (vector) for the input text.
        """
        res = self.post(endpoint='embedding', data={'embeddingType': embedding_type, 'model': model, 'text': text})
        return EmbeddingResponse(**res)

    def tokenize(self, text: str, model: str = 'general'):
        """Tokenize the input text.
        Args:
            model (str): The name of the model to use for tokenization.
                Currently only 'general' is supported.
            text (str): The input text to tokenize.

        Returns:
            tokens: The tokenized input text.
        """
        res = self.post(endpoint='tokenize', data={'model': model, 'text': text})
        return TokenizationResponse(**res)

    def generate_instruct(self, instruction_text: str,
                          instruction_uri: str = None,
                          request_text: str = None,
                          generation_options: GenerationOptions | dict = config.default_generation_options,
                          model: str = 'general',
                          temperature: float = None,
                          max_tokens: int = None,
                          partial_results: bool = None,
                          ):
        if isinstance(generation_options, dict):
            generation_options = GenerationOptions(**generation_options)

        # Model parameters override generation options
        if temperature is not None:
            generation_options.temperature = temperature
        if max_tokens is not None:
            generation_options.max_tokens = max_tokens
        if partial_results is not None:
            generation_options.partialResults = partial_results

        if (((instruction_uri is None) and (request_text is None)) or
                ((instruction_uri is not None) and (request_text is not None))):
            raise ValueError('includes only one of the fields instructionText, instructionUri')

        res = self.post(endpoint='instruct',
                        data={'instructionText': instruction_text,
                              'instructionUri': instruction_uri,
                              'requestText': request_text,
                              'model': model,
                              'generationOptions': generation_options.model_dump()})
        return GenerateTextInstructResponse(**res['result'])
