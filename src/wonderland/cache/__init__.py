from typing import Callable, TypeVar

from bs4 import BeautifulSoup

from .file_cache import FileCache, PostFileCache

T = TypeVar('T')

__all__ = [
    "PostFileCache",
    "FileCache",
    "title",
    "get",
]


def title(soup: BeautifulSoup) -> str:
    return soup.find(id='question-header').a.get_text()
