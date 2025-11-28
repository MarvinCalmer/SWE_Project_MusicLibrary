import json
import pytest
from pathlib import Path
from src.core.library import Library
from src.core.title import Title


# ============================================================================
# FIXTURES
# ============================================================================

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

# ============================================================================
# LOAD TESTS
# ============================================================================

class TestLoad:
    """Tests für Library.load() Methode."""

    def test_load_empty_library(self, empty_library):
        """Leere Library laden."""
        result = empty_library.load()
        
        assert isinstance(result, list), "load() sollte eine Liste zurückgeben"
        assert len(result) == 0, "Leere Library sollte leere Liste zurückgeben"
        assert len(empty_library.titles) == 0, "titles sollte leer sein"
        assert len(empty_library.get_titles()) == 0, "get_titles() sollte leer sein"

    def test_load_with_songs(self, library_with_songs):
        """Library mit Songs laden."""
        result = library_with_songs.load()
        
        assert isinstance(result, list), "load() sollte Liste zurückgeben"
        assert len(result) == 3, "Sollte 3 Titel enthalten"
        assert all(isinstance(t, Title) for t in result), "Alle Elemente sollten Title-Objekte sein"

    def test_load_preserves_all_fields(self, library_with_songs):
        """Alle Felder werden korrekt geladen."""
        titles = library_with_songs.get_titles()
        
        first_title = titles[0]
        assert first_title.id == 1
        assert first_title.name == "Imagine"
        assert first_title.artist == "John Lennon"
        assert first_title.album == "Imagine"
        assert first_title.year == 1971
        assert first_title.genre == "Rock"

    def test_load_nonexistent_file(self, tmp_path):
        """Nicht existierende Datei laden."""
        file_path = tmp_path / "nonexistent.json"
        lib = Library(filepath=file_path)
        
        assert lib.titles == [], "Sollte leere Liste bei nicht existierender Datei erstellen"

    def test_load_empty_json_object(self, tmp_path):
        """Leeres JSON-Objekt laden."""
        file_path = tmp_path / "empty_object.json"
        file_path.write_text("{}", encoding="utf-8")
        
        lib = Library(filepath=file_path)
        
        assert lib.titles == [], "Sollte leere Liste bei leerem JSON-Objekt erstellen"

# ============================================================================
# ADD TITLE TESTS
# ============================================================================

class TestAddTitle:
    """Tests für Library.add_title() Methode."""

    def test_add_title_to_empty_library(self, empty_library, sample_title):
        """Titel zu leerer Library hinzufügen."""
        result = empty_library.add_title(sample_title)

        assert isinstance(result, dict), "add_title() sollte dict zurückgeben"
        assert result["name"] == "Imagine", "Name sollte korrekt sein"
        assert len(empty_library.titles) == 1, "Library sollte 1 Titel enthalten"
        
        # JSON-Datei prüfen
        data = read_json(empty_library.filepath)
        assert len(data) == 1, "JSON sollte 1 Eintrag haben"
        assert data[0]["name"] == "Imagine"

    def test_add_title_auto_id_first(self, empty_library, sample_title):
        """Erste ID wird automatisch auf 1 gesetzt."""
        result = empty_library.add_title(sample_title)
        
        assert result["id"] == 1, "Erste ID sollte 1 sein"
        assert sample_title.id == 1, "Title-Objekt sollte ID 1 haben"

    def test_add_title_auto_id_increment(self, empty_library, sample_titles):
        """IDs werden automatisch inkrementiert."""
        for i, title in enumerate(sample_titles, start=1):
            result = empty_library.add_title(title)
            assert result["id"] == i

    def test_add_title_preserves_existing_id(self, empty_library):
        """Vorhandene ID wird nicht überschrieben."""
        title = Title(id=24, name="Test", artist="Artist", album="Album", year=2000, genre="Rock")
        result = empty_library.add_title(title)
        
        assert result["id"] == 24, "Vorhandene ID sollte erhalten bleiben"
        
        data = read_json(empty_library.filepath)
        assert data[0]["id"] == 24

    def test_add_multiple_titles(self, empty_library, sample_titles):
        """Mehrere Titel hinzufügen."""
        for title in sample_titles:
            empty_library.add_title(title)
        
        assert len(empty_library.titles) == 3, "Sollte 3 Titel enthalten"
        
        data = read_json(empty_library.filepath)
        assert len(data) == 3, "JSON sollte 3 Einträge haben"


    def test_add_title_with_empty_fields(self, empty_library):
        """Titel mit leeren Feldern hinzufügen."""
        title = Title(name="", artist="", album="", year=0, genre="")
        result = empty_library.add_title(title)
        
        assert result["id"] is not None, "ID sollte trotzdem gesetzt werden"
        assert result["name"] == ""

# ============================================================================
# UPDATE TITLE TESTS
# ============================================================================

class TestUpdateTitle:
    """Tests für Library.update_title() Methode."""

    def test_update_single_field(self, library_with_songs):
        """Einzelnes Feld aktualisieren."""
        result = library_with_songs.update_title(1, genre="Pop")
        
        assert result["genre"] == "Pop", "Genre sollte aktualisiert sein"
        assert result["name"] == "Imagine", "Name sollte unverändert sein"
        
        # JSON prüfen
        data = read_json(library_with_songs.filepath)
        assert data[0]["genre"] == "Pop"

    def test_update_multiple_fields(self, library_with_songs):
        """Mehrere Felder aktualisieren."""
        result = library_with_songs.update_title(
            1,
            name="New Name",
            artist="New Artist",
            year=2000
        )
        
        assert result["name"] == "New Name"
        assert result["artist"] == "New Artist"
        assert result["year"] == 2000
        assert result["album"] == "Imagine", "Nicht-aktualisierte Felder sollten gleich bleiben"

    def test_update_all_fields(self, library_with_songs):
        """Alle Felder aktualisieren."""
        result = library_with_songs.update_title(
            1,
            name="New",
            artist="Artist",
            album="Album",
            year=2024,
            genre="Pop"
        )
        
        assert result["name"] == "New"
        assert result["artist"] == "Artist"
        assert result["album"] == "Album"
        assert result["year"] == 2024
        assert result["genre"] == "Pop"
        assert result["id"] == 1, "ID sollte unverändert bleiben"



    def test_update_persists_after_reload(self, library_with_songs):
        """Update bleibt nach Reload erhalten."""
        library_with_songs.update_title(1, genre="Jazz")
        
        # Neu laden
        library_with_songs.load()
        
        title = library_with_songs.get_titles()[0]
        assert title.genre == "Jazz", "Update sollte nach Reload erhalten bleiben"

    def test_update_nonexistent_id_returns_none(self, library_with_songs):
        """Update mit nicht existierender ID."""
        # _find_index_by_id gibt None zurück, was zu IndexError führt
        with pytest.raises((IndexError, TypeError)):
            library_with_songs.update_title(999, name="Test")

# ============================================================================
# DELETE TITLE TESTS
# ============================================================================

class TestDeleteTitle:
    """Tests für Library.delete_title() Methode."""

    def test_delete_title(self, library_with_songs):
        """Titel löschen."""
        result = library_with_songs.delete_title(1)
        
        assert isinstance(result, dict), "Sollte gelöschtes Title-Dict zurückgeben"
        assert result["name"] == "Imagine"
        assert len(library_with_songs.titles) == 2, "Sollte noch 2 Titel haben"
        
        # JSON prüfen
        data = read_json(library_with_songs.filepath)
        assert len(data) == 2
        assert all(t["id"] != 1 for t in data), "ID 1 sollte nicht mehr existieren"

    def test_delete_middle_title(self, library_with_songs):
        """Mittleren Titel löschen."""
        library_with_songs.delete_title(2)
        
        remaining_ids = [t.id for t in library_with_songs.titles]
        assert remaining_ids == [1, 3], "IDs 1 und 3 sollten übrig bleiben"

    def test_delete_last_title(self, library_with_songs):
        """Letzten Titel löschen."""
        library_with_songs.delete_title(3)
        
        assert len(library_with_songs.titles) == 2
        assert library_with_songs.titles[-1].id == 2

    def test_delete_all_titles(self, library_with_songs):
        """Alle Titel nacheinander löschen."""
        library_with_songs.delete_title(1)
        library_with_songs.delete_title(2)
        library_with_songs.delete_title(3)
        
        assert len(library_with_songs.titles) == 0
        
        data = read_json(library_with_songs.filepath)
        assert len(data) == 0

    def test_delete_nonexistent_id(self, library_with_songs):
        """Nicht existierende ID löschen."""
        with pytest.raises((IndexError, TypeError)):
            library_with_songs.delete_title(999)


# ============================================================================
# SEARCH TESTS
# ============================================================================

class TestSearch:
    """Tests für Library.search_library() Methode."""

    def test_search_by_name(self, library_with_songs):
        """Nach Name suchen."""
        results = library_with_songs.search_library(name="Imagine")
        
        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0]["name"] == "Imagine"

    def test_search_case_insensitive(self, library_with_songs):
        """Suche ist case-insensitive."""
        results = library_with_songs.search_library(name="imagine")
        
        assert len(results) == 1
        assert results[0]["name"] == "Imagine"

    def test_search_partial_match(self, library_with_songs):
        """Partielle Übereinstimmung funktioniert."""
        results = library_with_songs.search_library(name="Jude")
        
        assert len(results) == 1
        assert results[0]["name"] == "Hey Jude"


    def test_search_multiple_filters(self, library_with_songs):
        """Mehrere Filter kombinieren."""
        results = library_with_songs.search_library(artist="John Lennon", year=1971)
        
        assert len(results) == 1
        assert results[0]["name"] == "Imagine"

    def test_search_no_results(self, library_with_songs):
        """Keine Ergebnisse finden."""
        results = library_with_songs.search_library(name="Nonexistent")
        
        assert isinstance(results, list)
        assert len(results) == 0

    def test_search_empty_library(self, empty_library):
        """In leerer Library suchen."""
        results = empty_library.search_library(name="Test")
        
        assert results == []

    def test_search_returns_sorted_results(self, library_with_songs):
        """Ergebnisse sind nach Name sortiert."""
        results = library_with_songs.search_library(genre="Rock")
        
        names = [r["name"] for r in results]
        assert names == sorted(names), "Ergebnisse sollten alphabetisch sortiert sein"

    def test_search_with_nonexistent_field(self, library_with_songs):
        """Suche mit nicht existierendem Feld."""
        results = library_with_songs.search_library(nonexistent_field="value")
        
        assert results == [], "Sollte leere Liste bei nicht existierendem Feld zurückgeben"

    def test_search_year_exact_match(self, library_with_songs):
        """Jahr muss exakt übereinstimmen (keine partielle Suche)."""
        results = library_with_songs.search_library(year=197)  # Partielle Jahreszahl
        
        assert len(results) == 0, "Jahreszahl sollte exakt übereinstimmen"


# ============================================================================
# GET METHODS TESTS
# ============================================================================

class TestGetMethods:
    """Tests für get_titles() und get_titles_by_id() Methoden."""

    def test_get_titles_returns_all(self, library_with_songs):
        """get_titles() gibt alle Titel zurück."""
        titles = library_with_songs.get_titles()
        
        assert isinstance(titles, list)
        assert len(titles) == 3
        assert all(isinstance(t, Title) for t in titles)

    def test_get_titles_empty_library(self, empty_library):
        """get_titles() bei leerer Library."""
        titles = empty_library.get_titles()
        
        assert titles == []

    def test_get_titles_by_id(self, library_with_songs):
        """get_titles_by_id() gibt korrekten Titel zurück."""
        title = library_with_songs.get_titles_by_id(0)
        
        assert isinstance(title, Title)
        assert title.name == "Imagine"

    def test_get_titles_by_id_last(self, library_with_songs):
        """Letzten Titel per Index abrufen."""
        title = library_with_songs.get_titles_by_id(-1)
        
        assert title.name == "Bohemian Rhapsody"

    def test_get_titles_by_id_out_of_range(self, library_with_songs):
        """Index außerhalb des Bereichs."""
        with pytest.raises(IndexError):
            library_with_songs.get_titles_by_id(999)

    def test_get_titles_by_id_negative_out_of_range(self, library_with_songs):
        """Negativer Index außerhalb des Bereichs."""
        with pytest.raises(IndexError):
            library_with_songs.get_titles_by_id(-999)

# ============================================================================
# PRIVATE METHODS TESTS
# ============================================================================

class TestPrivateMethods:
    """Tests für private Hilfsmethoden."""

    def test_find_index_by_id_existing(self, library_with_songs):
        """_find_index_by_id findet existierende ID."""
        index = library_with_songs._find_index_by_id(2)
        
        assert index == 1, "ID 2 sollte bei Index 1 sein"

    def test_find_index_by_id_nonexistent(self, library_with_songs):
        """_find_index_by_id gibt None bei nicht existierender ID."""
        index = library_with_songs._find_index_by_id(999)
        
        assert index is None

    def test_find_index_by_id_first(self, library_with_songs):
        """Erste ID finden."""
        index = library_with_songs._find_index_by_id(1)
        
        assert index == 0

    def test_find_index_by_id_last(self, library_with_songs):
        """Letzte ID finden."""
        index = library_with_songs._find_index_by_id(3)
        
        assert index == 2

    def test_refresh_titles_from_data(self, empty_library):
        """_refresh_titles_from_data aktualisiert titles-Liste."""
        data = [
            {"id": 1, "name": "Test", "artist": "Artist", "album": "Album", "year": 2000, "genre": "Rock"}
        ]
        
        empty_library._refresh_titles_from_data(data)
        
        assert len(empty_library.titles) == 1
        assert empty_library.titles[0].name == "Test"
