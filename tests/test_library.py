from core.library import Library
from core.title import Title
import json

def test_library_load_empty(tmp_path):
    lib = Library(filepath=tmp_path / "lib.json")
    result = lib.load()
    assert result["success"] is False
    assert len(lib.titles) == 0

def test_add_title_writes_single_file(tmp_path):
    file_path = tmp_path / "library.json"
    lib = Library(filepath=file_path)

    title = Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock")
    result = lib.add_title(title)

    # Prüfen: Rückgabewert
    assert result["success"] is True
    assert result["title"]["name"] == "Imagine"

    # Automatisch vergebene ID prüfen
    assert result["title"]["id"] == 1

    # Prüfen: Datei wurde erstellt
    assert file_path.exists()

    # Prüfen: Datei enthält genau den Titel
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["artist"] == "John Lennon"
    assert data[0]["year"] == 1971
    assert data[0]["id"] == 1

def test_update_title(tmp_path):
    file_path = tmp_path / "library.json"
    lib = Library(filepath=file_path)

    # Titel hinzufügen, ID wird automatisch gesetzt
    t1 = Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock")
    result_add = lib.add_title(t1)

    # ID aus dem Rückgabewert nutzen
    title_id = result_add["title"]["id"]

    # Update
    result = lib.update_title(title_id, genre="Pop", year=1972)

    assert result["success"] is True
    assert result["title"]["genre"] == "Pop"
    assert result["title"]["year"] == 1972

    # Prüfen: Dateiinhalt
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data[0]["id"] == title_id
    assert data[0]["genre"] == "Pop"
    assert data[0]["year"] == 1972
