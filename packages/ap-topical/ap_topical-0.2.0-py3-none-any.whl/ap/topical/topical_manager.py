import asyncio
import functools
from collections import defaultdict
from ap.topical import cache

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
                    asyncs.append(cb)
                else:
                    syncs.append(cb)
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
            def wrapped(fn):
                @functools.wraps(fn)
                def wrapper(payload):
                    # TODO: Time/other injection here
                    fn(payload)
                return wrapper

            return wrapped
