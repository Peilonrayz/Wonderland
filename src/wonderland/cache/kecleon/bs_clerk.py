import json
from typing import Tuple, Callable, Any

from bs4 import BeautifulSoup

from kecleon import FileClerk, Item
from kecleon.jobs import RawItem, FileItem


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
