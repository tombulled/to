from typing import Dict, List, TextIO

import thefuzz.fuzz
import yaml
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

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


@app.get("/")
def get_root() -> List[dict]:
    return load_db()


@app.get("/search")
def get_search(q: str) -> List[dict]:
    ratios: Dict[Bookmark, int] = {
        bookmark: ratio
        for bookmark in get_bookmarks()
        if (ratio := thefuzz.fuzz.ratio(bookmark.title, q)) > THRESHOLD
    }

    return sorted(ratios.keys(), key=ratios.get, reverse=True)
