from typing import Dict, List, TextIO

import thefuzz.fuzz
import yaml
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import furl

from .models import Bookmark

THRESHOLD: int = 33

app: FastAPI = FastAPI()

app.mount("/icons", StaticFiles(directory="icons"), name="icons")


def load_db() -> List[dict]:
    file: TextIO
    with open("config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def get_bookmarks() -> List[Bookmark]:
    return [Bookmark(**bookmark) for bookmark in load_db()]


def get_ratio(bookmark: Bookmark, query: str) -> int:
    return max(
        thefuzz.fuzz.ratio(source, query)
        for source in (
            bookmark.title,
            furl.furl(bookmark.url).host.replace(".", " ")
        )
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
