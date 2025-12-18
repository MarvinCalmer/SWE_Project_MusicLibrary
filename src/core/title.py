from dataclasses import dataclass


@dataclass
class Title:
    """
    Represents a single media title such as a song, book, or other library item.

    Attributes
    ----------
    id : int or None
        Unique identifier of the title. If None, the Library assigns an ID automatically.
    name : str
        The name or title of the media entry.
    artist : str
        The creator, performer, or author of the title.
    album : str
        Associated album or collection name.
    year : int
        Release or publication year.
    genre : str
        Genre classification of the media.
    """

    id: int
    name: str
    artist: str
    album: str
    year: int
    genre: str

    def __init__(
        self, id=None, name="", artist="", album="", year=0, genre="", is_favorite=False
    ):
        """
        Initialize a Title instance.

        Parameters
        ----------
        id : int or None, optional
            ID of the title. If None, the Library will assign an auto-incrementing ID.
        name : str, optional
            Name of the title.
        artist : str, optional
            Artist, creator, or author.
        album : str, optional
            Album or collection name.
        year : int, optional
            Release or publication year.
        genre : str, optional
            Genre classification.
        """
        self.id = id
        self.name = name
        self.artist = artist
        self.album = album
        self.year = year
        self.genre = genre
        self.is_favorite = is_favorite

    def to_dict(self):
        """
        Convert the Title object into a serializable dictionary.

        Returns
        -------
        dict
            A dictionary containing all title fields.
        """
        return {
            "id": self.id,
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "year": self.year,
            "genre": self.genre,
            "is_favorite": self.is_favorite,
        }
