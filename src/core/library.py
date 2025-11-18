from pathlib import Path
import json
from typing import List
from .title import Title
from .abstract_library import AbstractLibrary

class Library(AbstractLibrary):
    """
    Concrete implementation of the AbstractLibrary interface.
    This class manages a collection of Title objects stored in a JSON file.
    
    It provides methods for loading, searching, adding, updating, and deleting
    titles, as well as utility functions for file handling and ID management.
    """

    def __init__(self, filepath="library.json"):
        self.filepath = Path(filepath)
        self.titles: List[Title] = []
        self.load()

    def get_titles(self):
        return self.titles

    def get_titles_by_id(self,index=None):
        return self.titles[index]

    def search_library(self, **kwargs):
        # Ergebnisse filtern
        filtered = []
        for title in self.titles:
            match = True
            for key, value in kwargs.items():
                # Prüfen, ob das Attribut existiert
                if not hasattr(title, key):
                    match = False
                    break
                # Vergleich (case-insensitive für Strings)
                attr = getattr(title, key)
                if isinstance(attr, str) and isinstance(value, str):
                    if value.lower() not in attr.lower():
                        match = False
                        break
                else:
                    if attr != value:
                        match = False
                        break
            if match:
                filtered.append(title)
        filtered.sort(key=lambda t: getattr(t, 'name', str(t)))

        return [t.to_dict() for t in filtered]

    def load(self):
        data = self._load_file()
        if data is None:
            self.titles = []
        elif not data:
            self.titles = []
        else:
            self._refresh_titles_from_data(data)
        return self.titles

    def add_title(self, title: Title):
        if title.id is None:
            if self.titles:
                title.id = max(t.id for t in self.titles) + 1
            else:
                title.id = 1

        self.titles.append(title)
        data = [t.to_dict() for t in self.titles]
        self._save_file(data)

        return title.to_dict()

    def update_title(self, title_id: int, **kwargs):
        index = self._find_index_by_id(title_id)
        title_dict = self.titles[index].to_dict()

        for key, value in kwargs.items():
            title_dict[key] = value

        self.titles[index] = Title(**title_dict)
        data = [t.to_dict() for t in self.titles]
        self._save_file(data)

        return self.titles[index].to_dict()

    def delete_title(self, title_id: int):
        data = self._load_file()
        index = self._find_index_by_id(title_id)

        deleted_title = data.pop(index)
        self._save_file(data)
        self._refresh_titles_from_data(data)

        return deleted_title

    def _find_index_by_id(self, title_id: int):
        for i, t in enumerate(self.titles):
            if t.id == title_id:
                return i
        return None

    def _load_file(self):
        if not self.filepath.exists():
            return None
        with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # Datei existiert, aber ist ungültig
                return []
        return data

    def _save_file(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _refresh_titles_from_data(self, data):
        self.titles = [Title(**t) for t in data]
