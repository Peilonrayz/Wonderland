from typing import Callable, TypeVar

from bs4 import BeautifulSoup

from .file_cache import FileCache, BSFileCache

T = TypeVar('T')

__all__ = [
    "BSFileCache",
    "FileCache",
    "title",
    "get",
]


def title(soup: BeautifulSoup) -> str:
    return soup.find(id='question-header').a.get_text()


def get(id: int, fn: Callable[[BeautifulSoup], T]) -> T:
    return BSFileCache.from_file(fn)[id]
