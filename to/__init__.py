from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import List, TextIO
import yaml
import thefuzz.fuzz

app: FastAPI = FastAPI()

app.mount("/icons", StaticFiles(directory="icons"), name="icons")


def load_db() -> List[dict]:
    file: TextIO
    with open("config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


@app.get("/")
def get_root() -> List[dict]:
    return load_db()


@app.get("/search")
def get_search(q: str) -> List[dict]:
    return sorted(
        load_db(),
        key=lambda bookmark: thefuzz.fuzz.ratio(bookmark["title"], q),
        reverse=True,
    )
