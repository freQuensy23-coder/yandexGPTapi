import os
import unittest
from unittest import TestCase
from unittest.mock import patch

from dotenv import load_dotenv

from ygpt.api import YandexGPT


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.api = YandexGPT(iam_token=os.getenv('IAM_TOKEN'),
                             folder_id=os.getenv('FOLDER_ID'))

    def test_tokenize(self):
        text = 'Привет мир!'
        tokens = self.api.tokenize(text=text)
        self.assertIsNotNone(tokens)
        self.assertEqual(tokens.tokens[0].text, '<s>')
        self.assertEqual(len(tokens.tokens), 5)

    def test_embed(self):
        text = 'Привет мир!'
        embedding = self.api.embed(text=text, embedding_type='EMBEDDING_TYPE_QUERY')
        self.assertIsNotNone(embedding)
        self.assertEqual(len(embedding.embedding), 256)

    def test_generate_instruct(self):
        """Warning! This test can fail because of the model's randomness"""
        instruction = 'Напиши слово 5 раз'
        text = 'арбуз'
        response = self.api.generate_instruct(instruction_text=instruction,
                                              request_text=text,
                                              temperature=0.0)
        self.assertIn('арбуз', response.alternatives[0].text)


