from dataclasses import dataclass


@dataclass
class Playlist:
    """
    Represents a playlist containing references to Title objects.

    Attributes
    ----------
    id : int or None
        Unique identifier of the playlist.
    name : str
        Name of the playlist.
    description : str
        Optional description of the playlist.
    title_ids : List[int]
        List of title IDs that are in this playlist (references to Title objects).
    """

    def __init__(self, id=None, name="", description="", title_ids=None):
        """
        Initialize a Playlist instance.

        Parameters
        ----------
        id : int or None, optional
            ID of the playlist. If None, will be assigned automatically.
        name : str, optional
            Name of the playlist.
        description : str, optional
            Description of the playlist.
        title_ids : List[int], optional
            List of title IDs in the playlist.
        """
        self.id = id
        self.name = name
        self.description = description
        self.title_ids = title_ids if title_ids is not None else []

    def to_dict(self):
        """
        Convert the Playlist object into a serializable dictionary.

        Returns
        -------
        dict
            A dictionary containing all playlist fields.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "title_ids": self.title_ids,
        }
