import pytest
import json
import tempfile
import os
from src.core.library import Library
from src.core.title import Title
from src.core.playlist import Playlist
from src.core.playlist_manager import PlaylistManager


@pytest.fixture
def empty_library(tmp_path):
    """Erstellt eine leere Library mit temporärer JSON-Datei."""
    file_path = tmp_path / "lib.json"
    file_path.write_text("[]", encoding="utf-8")
    return Library(filepath=file_path)


@pytest.fixture
def library_with_songs(tmp_path):
    """Erstellt eine Library mit vordefinierten Songs."""
    file_path = tmp_path / "lib.json"
    json_data = [
        {
            "id": 1,
            "name": "Imagine",
            "artist": "John Lennon",
            "album": "Imagine",
            "year": 1971,
            "genre": "Rock",
        },
        {
            "id": 2,
            "name": "Hey Jude",
            "artist": "The Beatles",
            "album": "Hey Jude",
            "year": 1968,
            "genre": "Rock",
        },
        {
            "id": 3,
            "name": "Bohemian Rhapsody",
            "artist": "Queen",
            "album": "A Night at the Opera",
            "year": 1975,
            "genre": "Rock",
        },
    ]
    file_path.write_text(json.dumps(json_data), encoding="utf-8")
    return Library(filepath=file_path)


@pytest.fixture
def sample_title():
    """Erstellt ein Sample-Title-Objekt."""
    return Title(
        name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock"
    )


@pytest.fixture
def sample_titles():
    """Erstellt mehrere Sample-Title-Objekte."""
    return [
        Title(
            name="Imagine",
            artist="John Lennon",
            album="Imagine",
            year=1971,
            genre="Rock",
        ),
        Title(
            name="Hey Jude",
            artist="The Beatles",
            album="Hey Jude",
            year=1968,
            genre="Rock",
        ),
        Title(
            name="Smells Like Teen Spirit",
            artist="Nirvana",
            album="Nevermind",
            year=1991,
            genre="Grunge",
        ),
    ]


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


def read_json(path):
    """Helper: JSON-Datei einlesen."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class TestIntegration:
    """Integrationstests für komplexe Workflows."""

    def test_complete_crud_workflow(self, empty_library):
        """Kompletter CRUD-Workflow: Create, Read, Update, Delete."""
        # Create
        title = Title(
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            year=2024,
            genre="Rock",
        )
        added = empty_library.add_title(title)
        title_id = added["id"]

        # Read
        found = empty_library.search_library(name="Test Song")
        assert len(found) == 1

        # Update
        updated = empty_library.update_title(title_id, genre="Pop")
        assert updated["genre"] == "Pop"

        # Delete
        empty_library.delete_title(title_id)
        assert len(empty_library.titles) == 0

    def test_add_search_update_workflow(self, empty_library, sample_titles):
        """Hinzufügen, Suchen, Aktualisieren."""
        # Mehrere Titel hinzufügen
        for title in sample_titles:
            empty_library.add_title(title)

        # Nach Genre suchen
        rock_songs = empty_library.search_library(genre="Rock")
        assert len(rock_songs) == 2

        # Einen davon aktualisieren
        first_id = rock_songs[0]["id"]
        empty_library.update_title(first_id, genre="Classic Rock")

        # Erneut suchen
        classic_rock = empty_library.search_library(genre="Classic Rock")
        assert len(classic_rock) == 1

    def test_persistence_across_instances(self, tmp_path, sample_title):
        """Daten bleiben über Instanzen hinweg erhalten."""
        file_path = tmp_path / "persistent.json"

        # Erste Instanz: Titel hinzufügen
        lib1 = Library(filepath=file_path)
        lib1.add_title(sample_title)

        # Zweite Instanz: Titel sollte vorhanden sein
        lib2 = Library(filepath=file_path)
        assert len(lib2.titles) == 1
        assert lib2.titles[0].name == "Imagine"

    def test_id_continuity_after_delete(self, empty_library, sample_titles):
        """IDs werden nach Löschung korrekt fortgesetzt."""
        # 3 Titel hinzufügen (IDs: 1, 2, 3)
        for title in sample_titles:
            empty_library.add_title(title)

        # Titel 2 löschen
        empty_library.delete_title(2)

        # Neuen Titel hinzufügen - sollte ID 4 bekommen
        new_title = Title(
            name="New", artist="Artist", album="Album", year=2024, genre="Rock"
        )
        result = empty_library.add_title(new_title)

        assert result["id"] == 4, "Neue ID sollte max(existing_ids) + 1 sein"


class TestIntegrationPlaylist:
    """Integration tests for complete workflows."""

    def test_full_workflow(self, playlist_manager):
        """Test a complete workflow of playlist operations."""
        # Create playlist
        playlist = playlist_manager.create_playlist("My Playlist", "Description")
        assert playlist["id"] == 1

        # Add tracks
        playlist_manager.add_track(playlist["id"], 1)
        playlist_manager.add_track(playlist["id"], 2)
        playlist_manager.add_track(playlist["id"], 3)

        # Verify tracks
        result = playlist_manager.get_playlist(playlist["id"])
        assert len(result["title_ids"]) == 3

        # Remove a track
        playlist_manager.remove_track(playlist["id"], 2)
        result = playlist_manager.get_playlist(playlist["id"])
        assert result["title_ids"] == [1, 3]

        # Update playlist
        playlist_manager.update_playlist(playlist["id"], name="Updated Name")
        result = playlist_manager.get_playlist(playlist["id"])
        assert result["name"] == "Updated Name"

        # Delete playlist
        playlist_manager.delete_playlist(playlist["id"])
        assert len(playlist_manager.get_all_playlists()) == 0

    def test_multiple_playlists_with_same_tracks(self, playlist_manager):
        """Test that multiple playlists can reference the same tracks."""
        playlist1 = playlist_manager.create_playlist("Playlist 1")
        playlist2 = playlist_manager.create_playlist("Playlist 2")

        # Add same track to both playlists
        playlist_manager.add_track(playlist1["id"], 1)
        playlist_manager.add_track(playlist2["id"], 1)

        result1 = playlist_manager.get_playlist(playlist1["id"])
        result2 = playlist_manager.get_playlist(playlist2["id"])

        assert result1["title_ids"] == [1]
        assert result2["title_ids"] == [1]
