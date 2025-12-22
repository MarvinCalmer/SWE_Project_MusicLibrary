from pathlib import Path
import json
from typing import List, Optional
from .playlist import Playlist


class PlaylistManager:
    """
    Manages playlists that contain references to Title objects.

    This class provides methods for creating, deleting playlists,
    and adding/removing tracks (title references) to/from playlists.
    """

    def __init__(self, filepath="playlists.json"):
        """
        Initialize the PlaylistManager.

        Parameters
        ----------
        filepath : str, optional
            Path to the JSON file storing playlists.
        """
        self.filepath = Path(filepath)
        self.playlists: List[Playlist] = []
        self.load()

    def load(self):
        """Load playlists from the JSON file."""
        data = self._load_file()
        if data is None or not data:
            self.playlists = []
        else:
            self.playlists = [Playlist(**p) for p in data]
        return self.playlists

    def create_playlist(self, name: str, description: str = "") -> dict:
        """
        Create a new empty playlist.

        Parameters
        ----------
        name : str
            Name of the playlist.
        description : str, optional
            Description of the playlist.

        Returns
        -------
        dict
            Dictionary representation of the created playlist.
        """
        playlist = Playlist(name=name, description=description)

        # Auto-assign ID
        if self.playlists:
            playlist.id = max(p.id for p in self.playlists) + 1
        else:
            playlist.id = 1

        self.playlists.append(playlist)
        self._save_file()

        return playlist.to_dict()

    def delete_playlist(self, playlist_id: int) -> dict:
        """
        Delete a playlist by ID.

        Parameters
        ----------
        playlist_id : int
            ID of the playlist to delete.

        Returns
        -------
        dict
            Dictionary representation of the deleted playlist.

        Raises
        ------
        ValueError
            If playlist with given ID is not found.
        """
        index = self._find_index_by_id(playlist_id)

        if index is None:
            raise ValueError(f"Playlist with ID {playlist_id} not found")

        deleted_playlist = self.playlists.pop(index)
        self._save_file()

        return deleted_playlist.to_dict()

    def add_track(self, playlist_id: int, title_id: int) -> dict:
        """
        Add a track (title reference) to a playlist.

        Parameters
        ----------
        playlist_id : int
            ID of the playlist.
        title_id : int
            ID of the title to add.

        Returns
        -------
        dict
            Dictionary representation of the updated playlist.

        Raises
        ------
        ValueError
            If playlist is not found or title is already in the playlist.
        """
        index = self._find_index_by_id(playlist_id)

        if index is None:
            raise ValueError(f"Playlist with ID {playlist_id} not found")

        playlist = self.playlists[index]

        if title_id in playlist.title_ids:
            raise ValueError(f"Title with ID {title_id} is already in the playlist")

        playlist.title_ids.append(title_id)
        self._save_file()

        return playlist.to_dict()

    def remove_track(self, playlist_id: int, title_id: int) -> dict:
        """
        Remove a track (title reference) from a playlist.

        Parameters
        ----------
        playlist_id : int
            ID of the playlist.
        title_id : int
            ID of the title to remove.

        Returns
        -------
        dict
            Dictionary representation of the updated playlist.

        Raises
        ------
        ValueError
            If playlist is not found or title is not in the playlist.
        """
        index = self._find_index_by_id(playlist_id)

        if index is None:
            raise ValueError(f"Playlist with ID {playlist_id} not found")

        playlist = self.playlists[index]

        if title_id not in playlist.title_ids:
            raise ValueError(f"Title with ID {title_id} is not in the playlist")

        playlist.title_ids.remove(title_id)
        self._save_file()

        return playlist.to_dict()

    def get_playlist(self, playlist_id: int) -> Optional[dict]:
        """
        Get a playlist by ID.

        Parameters
        ----------
        playlist_id : int
            ID of the playlist.

        Returns
        -------
        dict or None
            Dictionary representation of the playlist, or None if not found.
        """
        index = self._find_index_by_id(playlist_id)

        if index is None:
            return None

        return self.playlists[index].to_dict()

    def get_all_playlists(self) -> List[dict]:
        """
        Get all playlists.

        Returns
        -------
        List[dict]
            List of all playlists as dictionaries.
        """
        return [p.to_dict() for p in self.playlists]

    def update_playlist(self, playlist_id: int, **kwargs) -> dict:
        """
        Update playlist metadata (name, description).

        Parameters
        ----------
        playlist_id : int
            ID of the playlist.
        **kwargs
            Fields to update (name, description).

        Returns
        -------
        dict
            Updated playlist dictionary.
        """
        index = self._find_index_by_id(playlist_id)

        if index is None:
            raise ValueError(f"Playlist with ID {playlist_id} not found")

        playlist = self.playlists[index]

        if "name" in kwargs:
            playlist.name = kwargs["name"]
        if "description" in kwargs:
            playlist.description = kwargs["description"]

        self._save_file()

        return playlist.to_dict()

    def _find_index_by_id(self, playlist_id: int) -> Optional[int]:
        """Find the index of a playlist by its ID."""
        for i, p in enumerate(self.playlists):
            if p.id == playlist_id:
                return i
        return None

    def _load_file(self):
        """Load data from the JSON file."""
        if not self.filepath.exists():
            return None

        with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
        return data

    def _save_file(self):
        """Save all playlists to the JSON file."""
        data = [p.to_dict() for p in self.playlists]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def export_playlist(self, playlist_id: int, export_path: str) -> bool:
        """
        Export a single playlist to a JSON file.

        Parameters
        ----------
        playlist_id : int
            ID of the playlist to export.
        export_path : str
            Path where the playlist should be exported.

        Returns
        -------
        bool
            True if export was successful.

        Raises
        ------
        ValueError
            If playlist with given ID is not found.
        """
        index = self._find_index_by_id(playlist_id)

        if index is None:
            raise ValueError(f"Playlist with ID {playlist_id} not found")

        playlist_data = self.playlists[index].to_dict()

        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(playlist_data, f, indent=4, ensure_ascii=False)

        return True

    def import_playlist(self, import_path: str) -> dict:
        """
        Import a playlist from a JSON file.

        Parameters
        ----------
        import_path : str
            Path to the JSON file containing the playlist.

        Returns
        -------
        dict
            Dictionary representation of the imported playlist.

        Raises
        ------
        ValueError
            If file cannot be read or contains invalid data.
        """
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                playlist_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Could not read playlist file: {e}")

        # Validate that required fields exist
        if not isinstance(playlist_data, dict):
            raise ValueError("Invalid playlist format")

        # Create new playlist with imported data (generate new ID)
        playlist = Playlist(
            id=None,  # Will be auto-assigned
            name=playlist_data.get("name", "Imported Playlist"),
            description=playlist_data.get("description", ""),
            title_ids=playlist_data.get("title_ids", []),
        )

        # Auto-assign ID
        if self.playlists:
            playlist.id = max(p.id for p in self.playlists) + 1
        else:
            playlist.id = 1

        self.playlists.append(playlist)
        self._save_file()

        return playlist.to_dict()
