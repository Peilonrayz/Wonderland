from typing import TypeVar

from bs4 import BeautifulSoup

from .file_cache import FileCache, PostFileCache, UserFileCache

T = TypeVar("T")

__all__ = [
    "PostFileCache",
    "UserFileCache",
    "FileCache",
    "title",
    "question_id",
    "user_name",
]


def title(soup: BeautifulSoup) -> str:
    return soup.find(id="question-header").a.get_text()


def question_id(soup: BeautifulSoup) -> str:
    return soup.find(id="question")["data-questionid"]


def user_name(soup: BeautifulSoup) -> str:
    return soup.find(class_="profile-user--name").get_text().strip()


def author_id(question_id: str, post_id: str) -> str:
    def author_id(soup: BeautifulSoup) -> str:
        id = "question" if question_id == post_id else f"answer-{post_id}"
        for detail in soup.find(id=id).find_all(class_="user-details")[::-1]:
            for a in detail.find_all("a"):
                href = a["href"]
                if href.startswith("/users/"):
                    return href[7:]
        if question_id == post_id:
            post_name = post_id
        else:
            post_name = f"{post_id} on question {question_id}"
        raise ValueError(f"No user found for {post_name}")
    return author_id


def post_license(q_id: str, id: str) -> str:
    def post_license(soup: BeautifulSoup) -> str:
        _id = "question" if q_id == id else f"answer-{id}"
        return soup.find(id=_id).find(class_="js-share-link")["data-se-share-sheet-license-name"]
    return post_license
