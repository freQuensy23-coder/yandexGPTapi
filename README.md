## Info 
![](https://avatars.mds.yandex.net/get-lpc/10704932/c244d2ce-b8a9-4821-83b3-63f32b45b808/orig)
This is simple api wrapper for [Yandex gpt api](https://cloud.yandex.ru/docs/yandexgpt/quickstart). 

## Installation
```bash
pip install git+https://github.com/freQuensy23-coder/yandexGPTapi.git
```

### Usage
1. Create your Yandex cloud, get access to yandex gpt, then [create iam token](https://cloud.yandex.ru/docs/iam/operations/iam-token/create)
2. Install this library
3. Create api instance and use it
```python
from ygpt.api import YandexGPT

api = YandexGPT(iam_token='your iam token', folder_id='your folder id')
text = 'This is very interesting film!!!'
text_vector = api.embed(text=text, embedding_type='EMBEDDING_TYPE_QUERY', model='general:embedding').embedding

instruction = 'You are ai assistant. You have to answer on user questions.'
text = 'What is the biggest plane in the world?'
print(api.generate_instruct(instruction_text=instruction, request_text=text).alternatives[0].text) 
# The biggest plane in the world is the Antonov An-225 Mriya, which has a wingspan of 366 feet and can carry up to 360...
```