import requests

class Watson(object):
    url = 'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2019-07-12'

    def __init__(self, api_key):
        self.api_key = api_key

    def analyze_body(self, body):
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'text': body,
            'features': {
                'categories': {
                    'limit': 10
                },
                'concepts': {},
                'entities': {},
                'keywords': {}
            }
        }

        response = requests.post(
            url=Watson.url,
            headers=headers,
            json=data,
            auth=('apikey', self.api_key)
        )

        return response