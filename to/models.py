import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True)
class Bookmark:
    title: str
    url: str
    description: str
    icon: str
    keywords: List[str] = dataclasses.field(default_factory=list)
