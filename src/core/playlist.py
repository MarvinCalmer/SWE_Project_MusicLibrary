from dataclasses import dataclass
from typing import List
from .title import Title


@dataclass
class Playlist:
    """
    Represents a Playlist which contains multiple Title objects
    """

    id: int | None
    titles: List[Title]

    def __init__(self, id=None, titles=None):
        self.id = id
        self.titles = titles if titles is not None else []

    def to_dict(self):
        return {"id": self.id, "titles": [title.to_dict() for title in self.titles]}
