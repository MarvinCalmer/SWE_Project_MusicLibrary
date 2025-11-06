from pathlib import Path
import json
from typing import List
from .title import Title

class Library:
    def __init__(self, filepath="library.json"):
        self.filepath = Path(filepath)
        self.titles: List[Title] = []

    def load(self):
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.titles = [Title(**t) for t in data]
            return {"success": True, "count": len(self.titles)}
        else:
            self.titles = []
            return {"success": False, "error": "File not found"}

    def add_title(self, title: Title):
        if title.id is None:
            if self.titles:
                title.id = max(t.id for t in self.titles) + 1
            else:
                title.id = 1

        # Titel zur Bibliothek hinzufügen
        self.titles.append(title)

        # Alle Titel als JSON speichern
        data = [t.to_dict() for t in self.titles]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return {"success": True, "count": len(self.titles), "title": title.to_dict()}

    def update_title(self, title_id: int, **kwargs):
        # Datei laden
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Titel mit passender ID finden
        found = None
        for i, t in enumerate(data):
            if t["id"] == title_id:
                found = i
                break

        # First search the JSON and 
        for key, value in kwargs.items():
            data[found][key] = value

        # Datei neu speichern
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        # Titelobjekte im Speicher aktualisieren
        self.titles = [Title(**t) for t in data]

        # Geänderten Titel zurückgeben
        return {"success": True, "title": data[found]}

    def delete_title(self, title_id: int):
        # Datei laden
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Titel mit passender ID finden
        found = None
        for i, t in enumerate(data):
            if t["id"] == title_id:
                found = i
                break

        # Titel suchen
        found = None
        for i, t in enumerate(data):
            if t["id"] == title_id:
                found = i
            break
        # Titel löschen
        deleted_title = data.pop(found)

        # Datei speichern
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        # interne Liste aktualisieren
        self.titles = [Title(**t) for t in data]

        return {"success": True, "title": deleted_title}
