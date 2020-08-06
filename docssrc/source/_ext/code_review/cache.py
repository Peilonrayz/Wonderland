import json
import time
from typing import Tuple, Callable, Any, TypeVar

from bs4 import BeautifulSoup

from kecleon import Store, FileClerk, WebClerk, Clerk, Item
from kecleon.jobs import RawItem, FileItem

T = TypeVar('T')


class BSClerk(FileClerk):
    def has_item(self, value: Tuple[str, Callable[[BeautifulSoup], Any]]):
        super().has_item(value[0])

    def get(self, value: Tuple[str, Callable[[BeautifulSoup], Any]]) -> FileItem:
        return super().get(value[0])

    def delete(self, value: Tuple[str, Callable[[BeautifulSoup], Any]]) -> None:
        super().delete(value[0])

    def set(self, value: Tuple[str, Callable[[BeautifulSoup], Any]], item: Item) -> None:
        """Set the cache to the item."""
        soup = BeautifulSoup(item.get_all(), 'html.parser')
        item = RawItem(json.dumps(value[1](soup)))
        super().set(value[0], item)


def title(soup: BeautifulSoup) -> str:
    return soup.find(id='question-header').a.get_text()


store = Store(
    warehouse=BSClerk(),
    deliveries=FileClerk(),
    provider=WebClerk(),
)


class FileCache(dict):
    CACHES = {}

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
    
        self[id] = value = json.loads(data)
        with open('.cache/' + self.fn.__name__ + '.json', 'w') as f:
            json.dump(self, f)
        print(id, len(self), id in self, self.get(id))
        
        global i
        i += 1
        print(i)
        time.sleep(10)
        return value


i = 0

def get(id: int, fn: Callable[[BeautifulSoup], T]) -> T:
    return FileCache.from_file(fn)[id]
