from typing import List, Set, TextIO

import thefuzz.fuzz
import yaml
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import furl
import re

from .models import Bookmark

app: FastAPI = FastAPI()

app.mount("/icons", StaticFiles(directory="icons"), name="icons")


def load_db() -> List[dict]:
    file: TextIO
    with open("assets/config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def get_bookmarks() -> List[Bookmark]:
    return [Bookmark(**bookmark) for bookmark in load_db()]


def extract_words(string: str) -> Set[str]:
    return {word.lower() for word in re.findall(r"[a-zA-Z]+", string)}


def get_words(bookmark: Bookmark) -> Set[str]:
    return (
        set(bookmark.keywords)
        | extract_words(furl.furl(bookmark.url).host.replace(".", " "))
        | extract_words(bookmark.title)
    )


def get_ratio(bookmark: Bookmark, query: str) -> int:
    return thefuzz.fuzz.partial_ratio(" ".join(get_words(bookmark)), query.lower())


@app.get("/")
def get_root() -> List[dict]:
    return load_db()


@app.get("/search")
def get_search(q: str) -> List[Bookmark]:
    return sorted(
        get_bookmarks(), key=lambda bookmark: get_ratio(bookmark, q), reverse=True
    )
