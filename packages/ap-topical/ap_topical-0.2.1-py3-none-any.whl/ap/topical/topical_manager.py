import asyncio
import functools
from collections import defaultdict

class TopicalManager:
    """
    Primary manager for pub/sub implementation
    """
    def __init__(self):
        self.__event_map = defaultdict(list)

    def subscribe(self, event, callback):
        self.__event_map[event].append(callback)

    def subscribe_many(self, mapping):
        for e, cs in mapping.items():
            [self.subscribe(e,c) for c in cs]

    def publish(self, event, payload):
        [callback(payload) for callback in self.__event_map[event] if not asyncio.iscoroutinefunction(callback)]

    async def publish_async(self, event, payload):
        [await callback(payload) for callback in self.__event_map[event] if asyncio.iscoroutinefunction(callback)]

    def list_callbacks(self):
        callback_map = {}

        for event, callbacks in self.__event_map.items():
            asyncs = []
            syncs = []
            for cb in callbacks:
                if asyncio.iscoroutinefunction(cb):
                    asyncs.append(cb.__name__)
                else:
                    syncs.append(cb.__name__)
            callback_map[event] = {
                'async': asyncs,
                'sync': syncs,
            }


        return callback_map

    class event:
        """
        Decorator class to ease building new eventing pipelines

        Usage:
            from ap.topical import topical

            @topical.event('event-name')
            async def my_func(payload):
                pass
        """
        def __init__(self, event):
            self.event = event
            self.decorator = self._decorator(event)

        def __call__(self, fn):
            return self.decorator(fn)

        def _decorator(self, event):
            from ap.topical import topical
            def wrapped(fn):

                if asyncio.iscoroutinefunction(fn):
                    @functools.wraps(fn)
                    async def wrapper(payload):
                        payload.access_by(f'{fn.__module__}.{fn.__qualname__}')
                        await fn(payload)

                else:
                    @functools.wraps(fn)
                    def wrapper(payload):
                        payload.access_by(f'{fn.__module__}.{fn.__qualname__}')
                        fn(payload)


                topical.subscribe(event, wrapper)
                return wrapper

            return wrapped

        def _inspect(self, fn):
            import inspect
