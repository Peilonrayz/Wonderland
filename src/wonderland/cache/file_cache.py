import json
import time
from typing import Any, Callable, TypeVar

from bs4 import BeautifulSoup

from .kecleon import store

T = TypeVar('T')


class FileCache(dict):
    CACHES = {}
    SLEEP = None

    @classmethod
    def from_file(cls, fn: Callable[[BeautifulSoup], T]) -> "FileCache":
        try:
            return cls.CACHES[fn.__name__]
        except KeyError:
            try:
                f = open('.cache/' + fn.__name__ + '.json')
            except FileNotFoundError:
                d = cls()
            else:
                with f:
                    d = cls(json.load(f))
            d.fn = fn
            return d
    
    def __missing__(self, id: int):
        self[id] = value = self._missing(id)
        print(id, len(self), id in self, self.get(id))
        with open('.cache/' + self.fn.__name__ + '.json', 'w') as f:
            json.dump(self, f)
        if self.SLEEP:
            time.sleep(self.SLEEP)
        return value

    def _missing(self, id: int) -> Any:
        raise ValueError(f'Unable to get item {id}')


class BSFileCache(FileCache):
    SLEEP = 10

    def _missing(self, id: int):
        try:
            line = (
                store
                    .line(
                        warehouse=(f'.cache/{self.fn.__name__}/{id}.json', self.fn),
                        deliveries=f'.cache/posts/{id}.html',
                        provider=f'https://codereview.meta.stackexchange.com/q/{id}',
                    )
            )
            data = line.get().get_all()
        except ValueError:
            raise ValueError(f'Unable to get item {id}')
        return json.loads(data)
