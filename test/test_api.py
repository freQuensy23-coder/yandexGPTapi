import os
from dotenv import load_dotenv
from ygpt import rest_adapter
from unittest import TestCase, mock


class TestRestAPIAdapter(TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.rest_adapter = rest_adapter.RestAdapter(iam_token=os.getenv('IAM_TOKEN'),
                                                     folder_id=os.getenv('FOLDER_ID'))

    def test_login(self):
        self.assertIsNotNone(self.rest_adapter.clouds)

    def test_wrong_iam_token(self):
        with self.assertRaises(ValueError):
            wrong_adapter = rest_adapter.RestAdapter(iam_token='wrong_token',
                                                     folder_id=os.getenv('FOLDER_ID'))

    def test_make_request(self):
        url = 'http://httpbin.org/get'
        response = self.rest_adapter._make_requests(method='GET', url=url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('requests.request')
    def test_post(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
                                                      "tokens": [
                                                        {
                                                          "id": "string",
                                                          "text": "string",
                                                          "special": True
                                                        }
                                                      ]}
        url = 'https://llm.api.cloud.yandex.net/llm/v1alpha/tokenize'
        response = self.rest_adapter._make_requests(method='GET', url=url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_request.return_value.json.return_value)

    @mock.patch('requests.request')
    def test_get(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
                                                      "tokens": [
                                                        {
                                                          "id": "string",
                                                          "text": "string",
                                                          "special": True
                                                        }
                                                      ]}
        url = 'https://llm.api.cloud.yandex.net/llm/v1alpha/tokenize'
        response = self.rest_adapter._make_requests(method='GET', url=url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_request.return_value.json.return_value)
        