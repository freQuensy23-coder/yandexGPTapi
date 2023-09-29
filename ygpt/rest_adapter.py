import re

from ygpt import config
import requests
from loguru import logger

from ygpt.utils.utils import try_or_none


class RestAdapter:
    def __init__(self,
                 iam_token: str,
                 folder_id: str = None,
                 ver: str = 'v1alpha',
                 ssl_verify: bool = True
                 ):
        """Base class for all REST API adapters. Just create url and send requests.
        :param iam_token: IAM token.
        See https://cloud.yandex.ru/docs/iam/operations/iam-token/create-for-federation for more info.
        :param folder_id: ID of the folder where the resource will be created. More here:
         https://cloud.yandex.com/en-ru/docs/resource-manager/operations/folder/get-id .
        :param ver: API version. Default: v1alpha
        :param ssl_verify: SSL verification. Default: True
        """
        self.url = config.hostname_format_string.format(
            version=ver,
        )
        self._iam_token = iam_token
        self._folder_id = folder_id
        self._ssl_verify = ssl_verify

        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

        clouds = self.login()
        if len(clouds) == 0:
            raise ValueError('No clouds found')
        self.clouds = clouds

    def login(self) -> dict:
        """Login to Yandex cloud and validate IAM token.
        :return: dict with clouds info, eg: [
              {
               "id": "b1g4ifm8d",
               "createdAt": "2022-04-05T12:26:05Z",
               "name": "cloude-1",
               "organizationId": "9li8rmaakm8co"
              },
              {
               "id": "b1gujaq7rt7mf2",
               "createdAt": "2023-08-23T09:42:09Z",
               "name": "dev",
               "organizationId": "9li8rmaakm8co"
              }
             ]
        """
        r = self._make_requests(method='GET',
                                url='https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds')

        if not 200 <= r.status_code <= 299:
            logger.warning(f'Login failed with status code {r.status_code}. {r.content}')
            if r.status_code == 401:
                logger.warning('Invalid IAM token')
                raise ValueError('Invalid IAM token')
            else:
                raise ValueError(f'Login failed with status code {r.status_code}. {r.content}')

        logger.info(f'Login success with status code {r.status_code}')
        clouds = r.json()['clouds']
        return clouds

    def _do(self, http_method: str, endpoint: str, ep_params: dict = None, data: dict = None):
        """Make requests to Yandex GPT2 API endpoint.
        :param http_method: HTTP method, eg: GET, POST, PUT, DELETE
        :param endpoint: API endpoint, eg: instruct, chat, embedding, tokenize
        :param ep_params: dict with params for endpoint
        :param data: dict with data for endpoint
        :return: dict with json data of response
        """
        response = self._make_requests(method=http_method,
                                       endpoint=endpoint,
                                       params=ep_params,
                                       json=data,
                                       verify=self._ssl_verify
                                       )
        if 200 <= response.status_code <= 299:  # OK
            return response.json()
        # message = r.json or r.content if json is Not available
        message = try_or_none(response.json) or response.content
        raise Exception(message)

    def _make_requests(self, method='GET', **kwargs):
        """Make requests with authentication headers.
        :param kwargs: kwargs for requests. It should contain 'service' or 'url' key.
        """
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        if 'endpoint' not in kwargs and 'url' not in kwargs:
            raise ValueError('endpoint or url must be specified')
        if "endpoint" not in kwargs:
            url = kwargs.pop('url', self.url)
        else:
            url = self.url.format(endpoint=kwargs['endpoint'])
            # remove endpoint from kwargs
            kwargs.pop('endpoint')

        # If auth headers not specified, add them
        if 'Authorization' not in kwargs['headers']:
            kwargs['headers'].update(self._get_auth_headers())

        logger.debug(f'Making request with method {method} and kwargs {kwargs}')
        result = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        logger.debug(f'Response result {result.content}')
        return result

    def get(self, endpoint: str, ep_params: dict = None) -> [dict]:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: dict = None, data: dict = None):
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)

    def _get_auth_headers(self):
        return {
            'Authorization': f'Bearer {self._iam_token}',
            'x-folder-id': self._folder_id
        }
