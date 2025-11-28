import json
import pytest
from pathlib import Path
from src.core.library import Library
from src.core.title import Title

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
        {"id": 1, "name": "Imagine", "artist": "John Lennon", "album": "Imagine", "year": 1971, "genre": "Rock"},
        {"id": 2, "name": "Hey Jude", "artist": "The Beatles", "album": "Hey Jude", "year": 1968, "genre": "Rock"},
        {"id": 3, "name": "Bohemian Rhapsody", "artist": "Queen", "album": "A Night at the Opera", "year": 1975, "genre": "Rock"}
    ]
    file_path.write_text(json.dumps(json_data), encoding="utf-8")
    return Library(filepath=file_path)


@pytest.fixture
def sample_title():
    """Erstellt ein Sample-Title-Objekt."""
    return Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock")


@pytest.fixture
def sample_titles():
    """Erstellt mehrere Sample-Title-Objekte."""
    return [
        Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock"),
        Title(name="Hey Jude", artist="The Beatles", album="Hey Jude", year=1968, genre="Rock"),
        Title(name="Smells Like Teen Spirit", artist="Nirvana", album="Nevermind", year=1991, genre="Grunge")
    ]


def read_json(path):
    """Helper: JSON-Datei einlesen."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class TestIntegration:
    """Integrationstests für komplexe Workflows."""

    def test_complete_crud_workflow(self, empty_library):
        """Kompletter CRUD-Workflow: Create, Read, Update, Delete."""
        # Create
        title = Title(name="Test Song", artist="Test Artist", album="Test Album", year=2024, genre="Rock")
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
        new_title = Title(name="New", artist="Artist", album="Album", year=2024, genre="Rock")
        result = empty_library.add_title(new_title)
        
        assert result["id"] == 4, "Neue ID sollte max(existing_ids) + 1 sein"

