import json
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
    assert isinstance(result, dict), "load() sollte ein dict zurückgeben"
    assert result.get("success") is False

    # JSON-Inhalt prüfen
    data = get_JSON(file_path)
    assert isinstance(data, list)
    assert len(data) == 0

    # Titel-Liste prüfen
    assert isinstance(lib.titles, list)
    assert len(lib.titles) == 0


def test_library_load_with_songs(tmp_path):
    # JSON-Datei mit Songs anlegen
    file_path = tmp_path / "lib.json"
    json_data = [
        {"name": "Imagine", "artist": "John Lennon", "album": "Imagine", "year": 1971, "genre": "Rock"},
        {"name": "Hey Jude", "artist": "The Beatles", "album": "Hey Jude", "year": 1968, "genre": "Rock"}
    ]
    file_path.write_text(json.dumps(json_data), encoding="utf-8")

    lib = Library(filepath=file_path)
    result = lib.load()

    # Rückgabewert prüfen
    assert isinstance(result, dict)
    assert result.get("success") is True
    assert result.get("count") == 2

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
        ("Hey Jude", "The Beatles", "Hey Jude", 1968, "Rock")
    ]
    assert titles == expected_titles

def test_add_title(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()
    title = Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock")
    result = lib.add_title(title)

    # Rückgabewert prüfen
    assert isinstance(result, dict)
    assert result.get("success") is True
    assert result.get("count") == 1

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

def test_edit_title(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()
    t1 = Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock")
    result_add = lib.add_title(t1)
    title_id = result_add["title"]["id"]
    result = lib.update_title(title_id, genre="test")

    # Rückgabewert prüfen
    assert isinstance(result, dict)
    assert result.get("success") is True

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

def test_delete_title(tmp_path):
    file_path = tmp_path / "lib.json"
    lib = Library(filepath=file_path)
    lib.load()
    t1 = Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock")
    t2 = Title(name="Hey Jude", artist="The Beatles", album="Single", year=1968, genre="Pop")
    result_add = lib.add_title(t2)
    lib.add_title(t1)
    title_id = result_add["title"]["id"]
    result = lib.delete_title(title_id)

    # Rückgabewert prüfen
    assert isinstance(result, dict)
    assert result.get("success") is True

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
