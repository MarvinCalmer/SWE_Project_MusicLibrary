from dataclasses import dataclass

@dataclass
class Title:
    id: int
    name: str
    artist: str
    album: str
    year: int
    genre: str

    def __init__(self, id=None, name="", artist="", album="", year=0, genre=""):
        self.id = id
        self.name = name
        self.artist = artist
        self.album = album
        self.year = year
        self.genre = genre


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "year": self.year,
            "genre": self.genre,
        }