import pytest
import json
import tempfile
import os
from pathlib import Path
from src.core.playlist import Playlist
from src.core.playlist_manager import PlaylistManager


# ==================== FIXTURES ====================


@pytest.fixture
def temp_playlist_file():
    """Create a temporary file for testing and clean up after."""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
    temp_file.close()
    temp_filepath = temp_file.name

    yield temp_filepath

    # Cleanup
    if os.path.exists(temp_filepath):
        os.unlink(temp_filepath)


@pytest.fixture
def playlist_manager(temp_playlist_file):
    """Create a PlaylistManager instance for testing."""
    return PlaylistManager(filepath=temp_playlist_file)


@pytest.fixture
def playlist_with_tracks(playlist_manager):
    """Create a playlist with some tracks already added."""
    playlist = playlist_manager.create_playlist("Test Playlist", "Test Description")
    playlist_manager.add_track(playlist["id"], 1)
    playlist_manager.add_track(playlist["id"], 2)
    playlist_manager.add_track(playlist["id"], 3)
    return playlist


@pytest.fixture
def multiple_playlists(playlist_manager):
    """Create multiple playlists for testing."""
    playlist1 = playlist_manager.create_playlist("First", "First Description")
    playlist2 = playlist_manager.create_playlist("Second", "Second Description")
    playlist3 = playlist_manager.create_playlist("Third", "Third Description")
    return [playlist1, playlist2, playlist3]


# ==================== PLAYLIST CLASS TESTS ====================


class TestPlaylist:
    """Test cases for the Playlist class."""

    def test_playlist_initialization_with_defaults(self):
        """Test playlist initialization with default values."""
        playlist = Playlist()
        assert playlist.id is None
        assert playlist.name == ""
        assert playlist.description == ""
        assert playlist.title_ids == []

    def test_playlist_initialization_with_values(self):
        """Test playlist initialization with specific values."""
        playlist = Playlist(
            id=1,
            name="Rock Classics",
            description="Best rock songs",
            title_ids=[1, 2, 3],
        )
        assert playlist.id == 1
        assert playlist.name == "Rock Classics"
        assert playlist.description == "Best rock songs"
        assert playlist.title_ids == [1, 2, 3]

    def test_playlist_to_dict(self):
        """Test converting playlist to dictionary."""
        playlist = Playlist(
            id=1, name="Test Playlist", description="Test", title_ids=[1, 2]
        )
        result = playlist.to_dict()

        expected = {
            "id": 1,
            "name": "Test Playlist",
            "description": "Test",
            "title_ids": [1, 2],
        }
        assert result == expected

    def test_playlist_empty_title_ids(self):
        """Test that title_ids defaults to empty list."""
        playlist = Playlist(id=1, name="Empty")
        assert playlist.title_ids == []
        assert isinstance(playlist.title_ids, list)


# ==================== PLAYLIST MANAGER TESTS ====================


class TestPlaylistManagerInitialization:
    """Test PlaylistManager initialization."""

    def test_initialization_with_nonexistent_file(self, playlist_manager):
        """Test initialization when file doesn't exist."""
        assert len(playlist_manager.playlists) == 0

    def test_initialization_creates_file_on_save(
        self, playlist_manager, temp_playlist_file
    ):
        """Test that file is created when saving."""
        playlist_manager.create_playlist("Test", "Description")
        assert os.path.exists(temp_playlist_file)


class TestCreatePlaylist:
    """Test playlist creation."""

    def test_create_playlist_basic(self, playlist_manager):
        """Test creating a basic playlist."""
        result = playlist_manager.create_playlist("My Playlist", "My Description")

        assert result["id"] == 1
        assert result["name"] == "My Playlist"
        assert result["description"] == "My Description"
        assert result["title_ids"] == []

    def test_create_playlist_without_description(self, playlist_manager):
        """Test creating a playlist without description."""
        result = playlist_manager.create_playlist("No Description")

        assert result["name"] == "No Description"
        assert result["description"] == ""

    def test_create_multiple_playlists_auto_increment_id(self, playlist_manager):
        """Test that IDs auto-increment correctly."""
        playlist1 = playlist_manager.create_playlist("First")
        playlist2 = playlist_manager.create_playlist("Second")
        playlist3 = playlist_manager.create_playlist("Third")

        assert playlist1["id"] == 1
        assert playlist2["id"] == 2
        assert playlist3["id"] == 3

    def test_create_playlist_persists_to_file(
        self, playlist_manager, temp_playlist_file
    ):
        """Test that created playlist is saved to file."""
        playlist_manager.create_playlist("Persisted", "Test")

        with open(temp_playlist_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["name"] == "Persisted"


class TestGetPlaylist:
    """Test playlist Getting."""

    def test_get_playlist_existing(self, playlist_manager):
        """Test getting an existing playlist."""
        created = playlist_manager.create_playlist("Test")
        result = playlist_manager.get_playlist(created["id"])

        assert result is not None
        assert result["name"] == "Test"

    def test_get_playlist_nonexistent(self, playlist_manager):
        """Test getting a non-existent playlist."""
        result = playlist_manager.get_playlist(999)
        assert result is None

    def test_get_all_playlists_empty(self, playlist_manager):
        """Test getting all playlists when none exist."""
        result = playlist_manager.get_all_playlists()
        assert result == []

    def test_get_all_playlists_multiple(self, multiple_playlists, playlist_manager):
        """Test getting all playlists when multiple exist."""
        result = playlist_manager.get_all_playlists()
        assert len(result) == 3
        assert result[0]["name"] == "First"
        assert result[1]["name"] == "Second"
        assert result[2]["name"] == "Third"


class TestUpdatePlaylist:
    """Test playlist updates."""

    def test_update_playlist_name(self, playlist_manager):
        """Test updating playlist name."""
        playlist = playlist_manager.create_playlist("Old Name", "Description")
        result = playlist_manager.update_playlist(playlist["id"], name="New Name")

        assert result["name"] == "New Name"
        assert result["description"] == "Description"

    def test_update_playlist_description(self, playlist_manager):
        """Test updating playlist description."""
        playlist = playlist_manager.create_playlist("Name", "Old Description")
        result = playlist_manager.update_playlist(
            playlist["id"], description="New Description"
        )

        assert result["name"] == "Name"
        assert result["description"] == "New Description"

    def test_update_playlist_both_fields(self, playlist_manager):
        """Test updating both name and description."""
        playlist = playlist_manager.create_playlist("Old", "Old Desc")
        result = playlist_manager.update_playlist(
            playlist["id"], name="New", description="New Desc"
        )

        assert result["name"] == "New"
        assert result["description"] == "New Desc"

    def test_update_nonexistent_playlist(self, playlist_manager):
        """Test updating a non-existent playlist raises error."""
        with pytest.raises(ValueError, match="not found"):
            playlist_manager.update_playlist(999, name="Test")


class TestDeletePlaylist:
    """Test playlist deletion."""

    def test_delete_playlist_existing(self, playlist_manager):
        """Test deleting an existing playlist."""
        playlist = playlist_manager.create_playlist("To Delete")
        result = playlist_manager.delete_playlist(playlist["id"])

        assert result["name"] == "To Delete"
        assert len(playlist_manager.get_all_playlists()) == 0

    def test_delete_playlist_nonexistent(self, playlist_manager):
        """Test deleting a non-existent playlist raises error."""
        with pytest.raises(ValueError, match="not found"):
            playlist_manager.delete_playlist(999)

    def test_delete_playlist_persists(self, playlist_manager, temp_playlist_file):
        """Test that deletion is persisted to file."""
        playlist = playlist_manager.create_playlist("To Delete")
        playlist_manager.delete_playlist(playlist["id"])

        # Reload from file
        new_manager = PlaylistManager(filepath=temp_playlist_file)
        assert len(new_manager.get_all_playlists()) == 0


class TestAddTrack:
    """Test adding tracks to playlists."""

    def test_add_track_to_empty_playlist(self, playlist_manager):
        """Test adding a track to an empty playlist."""
        playlist = playlist_manager.create_playlist("Test")
        result = playlist_manager.add_track(playlist["id"], 1)

        assert result["title_ids"] == [1]

    def test_add_multiple_tracks(self, playlist_manager):
        """Test adding multiple tracks to a playlist."""
        playlist = playlist_manager.create_playlist("Test")
        playlist_manager.add_track(playlist["id"], 1)
        playlist_manager.add_track(playlist["id"], 2)
        result = playlist_manager.add_track(playlist["id"], 3)

        assert result["title_ids"] == [1, 2, 3]

    def test_add_track_to_nonexistent_playlist(self, playlist_manager):
        """Test adding a track to non-existent playlist raises error."""
        with pytest.raises(ValueError, match="not found"):
            playlist_manager.add_track(999, 1)

    def test_add_duplicate_track(self, playlist_manager):
        """Test adding a duplicate track raises error."""
        playlist = playlist_manager.create_playlist("Test")
        playlist_manager.add_track(playlist["id"], 1)

        with pytest.raises(ValueError, match="already in the playlist"):
            playlist_manager.add_track(playlist["id"], 1)

    def test_add_track_persists(self, playlist_manager, temp_playlist_file):
        """Test that adding track is persisted to file."""
        playlist = playlist_manager.create_playlist("Test")
        playlist_manager.add_track(playlist["id"], 5)

        # Reload from file
        new_manager = PlaylistManager(filepath=temp_playlist_file)
        result = new_manager.get_playlist(playlist["id"])
        assert result["title_ids"] == [5]


class TestRemoveTrack:
    """Test removing tracks from playlists."""

    def test_remove_track_existing(self, playlist_with_tracks, playlist_manager):
        """Test removing an existing track."""
        result = playlist_manager.remove_track(playlist_with_tracks["id"], 1)
        assert result["title_ids"] == [2, 3]

    def test_remove_track_nonexistent_playlist(self, playlist_manager):
        """Test removing track from non-existent playlist raises error."""
        with pytest.raises(ValueError, match="not found"):
            playlist_manager.remove_track(999, 1)

    def test_remove_track_not_in_playlist(self, playlist_with_tracks, playlist_manager):
        """Test removing a track that's not in playlist raises error."""
        with pytest.raises(ValueError, match="not in the playlist"):
            playlist_manager.remove_track(playlist_with_tracks["id"], 999)

    def test_remove_track_persists(
        self, playlist_with_tracks, playlist_manager, temp_playlist_file
    ):
        """Test that removing track is persisted to file."""
        playlist_manager.remove_track(playlist_with_tracks["id"], 1)

        # Reload from file
        new_manager = PlaylistManager(filepath=temp_playlist_file)
        result = new_manager.get_playlist(playlist_with_tracks["id"])
        assert result["title_ids"] == [2, 3]

    def test_remove_all_tracks(self, playlist_with_tracks, playlist_manager):
        """Test removing all tracks from a playlist."""
        playlist_manager.remove_track(playlist_with_tracks["id"], 1)
        playlist_manager.remove_track(playlist_with_tracks["id"], 2)
        result = playlist_manager.remove_track(playlist_with_tracks["id"], 3)

        assert result["title_ids"] == []


class TestLoadSave:
    """Test loading and saving functionality."""

    def test_load_from_existing_file(self, playlist_manager, temp_playlist_file):
        """Test loading playlists from an existing file."""
        playlist_manager.create_playlist("First", "Desc1")
        playlist_manager.create_playlist("Second", "Desc2")

        # Create new manager with same file
        new_manager = PlaylistManager(filepath=temp_playlist_file)

        assert len(new_manager.playlists) == 2
        assert new_manager.playlists[0].name == "First"
        assert new_manager.playlists[1].name == "Second"

    def test_load_from_corrupted_file(self, temp_playlist_file):
        """Test loading from a corrupted JSON file."""
        # Write invalid JSON
        with open(temp_playlist_file, "w") as f:
            f.write("{ invalid json")

        # Should handle gracefully
        manager = PlaylistManager(filepath=temp_playlist_file)
        assert len(manager.playlists) == 0

    def test_load_from_empty_file(self, temp_playlist_file):
        """Test loading from an empty JSON file."""
        with open(temp_playlist_file, "w") as f:
            f.write("[]")

        manager = PlaylistManager(filepath=temp_playlist_file)
        assert len(manager.playlists) == 0
