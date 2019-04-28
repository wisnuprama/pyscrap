import json


def deserialize_cookies(json_path: str) -> dict:
    cookies = {}
    with open(json_path, 'r') as j:
        data = json.load(j)
        for d in data:
            cookies[d.get('name')] = d.get('value')
    return cookies
