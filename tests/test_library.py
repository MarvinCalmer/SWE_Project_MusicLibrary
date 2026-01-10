import json
import pytest
from src.core.library import Library
from src.core.title import Title


# Utility functions
def get_JSON(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def test_library_load_empty(tmp_path):
    file_path = tmp_path / "lib.json"
    file_path.write_text("[]", encoding="utf-8")

    lib = Library(filepath=file_path)
    result = lib.load()

    # Rückgabewert prüfen
    assert result == []
    assert isinstance(result, list), "load() sollte ein dict zurückgeben"

    # JSON-Inhalt prüfen
    data = get_JSON(file_path)
    assert isinstance(data, list)
    assert len(data) == 0

    # Titel-Liste prüfen
    assert isinstance(lib.titles, list)
    assert len(lib.titles) == 0

    assert isinstance(lib.get_titles(), list)
    assert len(lib.get_titles()) == 0


def test_library_load_with_songs(tmp_path):
    # JSON-Datei mit Songs anlegen
    file_path = tmp_path / "lib.json"
    json_data = [
        {
            "name": "Imagine",
            "artist": "John Lennon",
            "album": "Imagine",
            "year": 1971,
            "genre": "Rock",
        },
        {
            "name": "Hey Jude",
            "artist": "The Beatles",
            "album": "Hey Jude",
            "year": 1968,
            "genre": "Rock",
        },
    ]
    file_path.write_text(json.dumps(json_data), encoding="utf-8")

    lib = Library(filepath=file_path)
    result = lib.load()

    # Rückgabewert prüfen
    assert isinstance(result, list)
    assert len(result) == 2

    # JSON-Inhalt prüfen
    data = get_JSON(file_path)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Imagine"

    # Titel-Liste prüfen
    assert isinstance(lib.titles, list)
    titles = [(t.name, t.artist, t.album, t.year, t.genre) for t in lib.titles]
    expected_titles = [
        ("Imagine", "John Lennon", "Imagine", 1971, "Rock"),
        ("Hey Jude", "The Beatles", "Hey Jude", 1968, "Rock"),
    ]
    assert titles == expected_titles


def test_add_title(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()
    title = Title(
        name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock"
    )
    result = lib.add_title(title)

    # Rückgabewert prüfen
    assert isinstance(result, dict)
    assert "rating" in result
    assert result["rating"] is None

    # JSON-Inhalt prüfen
    data = get_JSON(file_path)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Imagine"
    assert data[0].get("rating") is None

    # Titel-Liste prüfen
    assert isinstance(lib.titles, list)
    titles = [(t.name, t.artist, t.album, t.year, t.genre) for t in lib.titles]
    expected_titles = [
        ("Imagine", "John Lennon", "Imagine", 1971, "Rock"),
    ]
    assert titles == expected_titles


def test_add_title_auto_id(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    t = Title(
        name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock"
    )

    result = lib.add_title(t)

    # Rückgabe prüfen
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["name"] == "Imagine"

    # JSON-Datei prüfen
    data = get_JSON(file_path)
    assert len(data) == 1
    assert data[0]["id"] == 1

    # interne Liste prüfen
    assert len(lib.titles) == 1
    assert lib.titles[0].name == "Imagine"


def test_add_title_increment_id(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    t1 = Title(name="Song A", artist="Artist A", album="A", year=2000, genre="Rock")
    t2 = Title(name="Song B", artist="Artist B", album="B", year=2001, genre="Pop")

    lib.add_title(t1)
    result2 = lib.add_title(t2)

    assert result2["id"] == 2

    data = get_JSON(file_path)
    assert len(data) == 2
    assert data[1]["id"] == 2


def test_add_title_preserves_existing_id(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    t = Title(
        name="Imagine",
        artist="John Lennon",
        album="Imagine",
        year=1971,
        genre="Rock",
        id=10,
    )

    result = lib.add_title(t)

    assert result["id"] == 10  # ID bleibt
    data = get_JSON(file_path)
    assert data[0]["id"] == 10


def test_edit_title(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()
    t1 = Title(
        name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock"
    )
    result_add = lib.add_title(t1)
    title_id = result_add["id"]
    result = lib.update_title(title_id, genre="test")

    # Rückgabewert prüfen
    assert isinstance(result, dict)

    # JSON-Inhalt prüfen
    data = get_JSON(file_path)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["genre"] == "test"

    # Titel-Liste prüfen
    assert isinstance(lib.titles, list)
    titles = [(t.name, t.artist, t.album, t.year, t.genre) for t in lib.titles]
    expected_titles = [
        ("Imagine", "John Lennon", "Imagine", 1971, "test"),
    ]
    assert titles == expected_titles


def test_update_title_multiple_fields(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    t = Title(
        name="Song A", artist="Artist A", album="Album A", year=2000, genre="Rock"
    )
    added = lib.add_title(t)
    title_id = added["id"]

    updated = lib.update_title(title_id, name="Song B", album="Album B", genre="Pop")

    assert updated["name"] == "Song B"
    assert updated["album"] == "Album B"
    assert updated["genre"] == "Pop"
    assert updated["year"] == 2000  # unchanged


def test_delete_title(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()
    t1 = Title(
        name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock"
    )
    t2 = Title(
        name="Hey Jude", artist="The Beatles", album="Single", year=1968, genre="Pop"
    )
    result_add = lib.add_title(t2)
    lib.add_title(t1)
    title_id = result_add["id"]
    result = lib.delete_title(title_id)

    # Rückgabewert prüfen
    assert isinstance(result, dict)

    # JSON-Inhalt prüfen
    data = get_JSON(file_path)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Imagine"

    # Titel-Liste prüfen
    assert isinstance(lib.titles, list)
    titles = [(t.name, t.artist, t.album, t.year, t.genre) for t in lib.titles]
    expected_titles = [
        ("Imagine", "John Lennon", "Imagine", 1971, "Rock"),
    ]
    assert titles == expected_titles


def test_search_library_by_name(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    t1 = Title(
        name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock"
    )
    t2 = Title(
        name="Hey Jude", artist="The Beatles", album="Single", year=1968, genre="Pop"
    )

    lib.add_title(t1)
    lib.add_title(t2)

    results = lib.search_library(name="Imagine")

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["name"] == "Imagine"


def test_search_library_case_insensitive(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    lib.add_title(
        Title(
            name="IMAGINE",
            artist="John Lennon",
            album="Imagine",
            year=1971,
            genre="Rock",
        )
    )

    results = lib.search_library(name="imagine")

    assert len(results) == 1
    assert results[0]["name"] == "IMAGINE"


def test_search_library_multiple_filters(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    lib.add_title(
        Title(
            name="Imagine",
            artist="John Lennon",
            album="Imagine",
            year=1971,
            genre="Rock",
        )
    )
    lib.add_title(
        Title(
            name="Imagine",
            artist="A Perfect Circle",
            album="Emotive",
            year=2004,
            genre="Alternative",
        )
    )

    results = lib.search_library(name="Imagine", year=1971)

    assert len(results) == 1
    assert results[0]["artist"] == "John Lennon"


def test_search_library_no_results(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    lib.add_title(
        Title(
            name="Imagine",
            artist="John Lennon",
            album="Imagine",
            year=1971,
            genre="Rock",
        )
    )

    results = lib.search_library(name="xyz")

    assert isinstance(results, list)
    assert len(results) == 0


def test_search_library_year(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    lib.add_title(
        Title(
            name="Imagine",
            artist="John Lennon",
            album="Imagine",
            year=1971,
            genre="Rock",
        )
    )

    results = lib.search_library(year=1971)

    assert len(results) == 1
    assert results[0]["name"] == "Imagine"


def test_title_default_not_favorite(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    t = Title(
        name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock"
    )
    lib.add_title(t)

    stored_title = lib.get_titles()[0]
    assert stored_title.is_favorite is False



def test_set_and_persist_rating(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    t = Title(
        name="Song A",
        artist="Artist A",
        album="Album A",
        year=2000,
        genre="Pop",
        rating=4,
    )
    lib.add_title(t)

    data = get_JSON(file_path)
    assert data[0]["rating"] == 4

    # Re-load library from file and check rating persisted
    lib2 = Library(filepath=file_path)
    lib2.load()

    assert lib2.get_titles()[0].rating == 4


def test_invalid_rating_raises(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()

    t = Title(
        name="Song",
        artist="A",
        album="B",
        year=2001,
        genre="Pop",
    )
    lib.add_title(t)

    with pytest.raises(ValueError):
        lib.update_title(1, rating=6)

    with pytest.raises(ValueError):
        Title(name="X", artist="Y", album="", year=0, genre="", rating=0)

    def test_toggle_favorite_unsets_favorite(tmp_path):
        file_path = tmp_path / "lib.json"
        lib = Library(filepath=file_path)
        lib.load()

        t = Title(name="Song", artist="Artist", album="Album", year=2020, genre="Pop")
        result = lib.add_title(t)

        lib.toggle_favorite(result["id"])
        new_status = lib.toggle_favorite(result["id"])

        assert new_status is False
        assert lib.get_titles()[0].is_favorite is False

    def test_favorite_persisted_after_reload(tmp_path):
        file_path = tmp_path / "lib.json"

        lib1 = Library(filepath=file_path)
        lib1.load()

        t = Title(name="Song", artist="Artist", album="Album", year=2020, genre="Pop")
        result = lib1.add_title(t)
        lib1.toggle_favorite(result["id"])

        # neue Instanz = Neustart
        lib2 = Library(filepath=file_path)
        titles = lib2.get_titles()

        assert titles[0].is_favorite is True
