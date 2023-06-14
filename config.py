import json


def get(key):
    with open('config.json') as f:
        data = json.load(f)
    return data[key]
