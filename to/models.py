import dataclasses


@dataclasses.dataclass(frozen=True)
class Bookmark:
    title: str
    url: str
    description: str
    icon: str
