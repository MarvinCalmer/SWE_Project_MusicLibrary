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

class TestEdgeCases:
    """Tests für Edge-Cases und Fehlerfälle."""

    def test_add_title_with_very_long_strings(self, empty_library):
        """Titel mit sehr langen Strings."""
        long_string = "A" * 10000
        title = Title(name=long_string, artist="Artist", album="Album", year=2000, genre="Rock")
        
        result = empty_library.add_title(title)
        
        assert result["name"] == long_string
        
        # Reload und prüfen
        empty_library.load()
        assert empty_library.titles[0].name == long_string

    def test_search_with_empty_string(self, library_with_songs):
        """Suche mit leerem String."""
        results = library_with_songs.search_library(name="")
        
        # Leerer String matched alles
        assert len(results) == 3

    def test_update_with_no_changes(self, library_with_songs):
        """Update ohne Änderungen."""
        original = library_with_songs.titles[0].to_dict()
        result = library_with_songs.update_title(1)
        
        assert result == original, "Sollte unverändert bleiben"

    def test_multiple_rapid_operations(self, empty_library, sample_titles):
        """Viele schnelle Operationen hintereinander."""
        # 100 Titel hinzufügen
        for i in range(100):
            title = Title(name=f"Song {i}", artist="Artist", album="Album", year=2000, genre="Rock")
            empty_library.add_title(title)
        
        assert len(empty_library.titles) == 100
        
        # Jeden zweiten löschen
        for i in range(1, 101, 2):
            empty_library.delete_title(i)
        
        assert len(empty_library.titles) == 50
