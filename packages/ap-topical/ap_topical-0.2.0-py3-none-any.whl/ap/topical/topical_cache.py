from uuid import uuid4

class TopicalCache:
    def __init__(self):
        self.__cache = {}

    def add(self, idempotency_token, event, callback):
        key = f'{idempotency_token}|{event}|{id(callback)}'

        if key in self.__cache.values():
            raise KeyError(f'key already exists in cache: {key}')

        guid = uuid4()
        self.__cache[guid] = key

        return guid
