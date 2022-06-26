from typing import Dict, List, Set, TextIO

import thefuzz.fuzz
import yaml
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import furl
import re

from .models import Bookmark

THRESHOLD: int = 15

app: FastAPI = FastAPI()

app.mount("/icons", StaticFiles(directory="icons"), name="icons")


def load_db() -> List[dict]:
    file: TextIO
    with open("config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def get_bookmarks() -> List[Bookmark]:
    return [Bookmark(**bookmark) for bookmark in load_db()]

def extract_words(string: str) -> Set[str]:
    return set(re.findall(r'[a-zA-Z]+', string))

def get_words(bookmark: Bookmark) -> Set[str]:
    return extract_words(bookmark.title) | extract_words(bookmark.description) | extract_words(furl.furl(bookmark.url).host.replace(".", " "))

def get_ratio(bookmark: Bookmark, query: str) -> int:
    return max(
        thefuzz.fuzz.ratio(word.lower(), query.lower())
        for word in get_words(bookmark)
    )


@app.get("/")
def get_root() -> List[dict]:
    return load_db()


@app.get("/search")
def get_search(q: str) -> List[dict]:
    ratios: Dict[Bookmark, int] = {
        bookmark: ratio
        for bookmark in get_bookmarks()
        if (ratio := get_ratio(bookmark, q)) > THRESHOLD
    }

    return sorted(ratios.keys(), key=ratios.get, reverse=True)
