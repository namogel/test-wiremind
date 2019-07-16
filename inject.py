from urllib.parse import quote, unquote
import json


def request(flow):
    if (
        'https://www.transavia.com/cczkbrpmtnvieywa.js' in flow.request.url and
        flow.request.method == 'POST'
    ):
        payload = json.loads(unquote(flow.request.content.decode())[2:])
        payload['fp2']['browser']['webdriver'] = False
        flow.request.content = quote('p=' + json.dumps(payload)).encode()
