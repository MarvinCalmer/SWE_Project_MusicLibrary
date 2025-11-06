from pathlib import Path
import json
from typing import List
from .title import Title

class Library:
    def __init__(self, filepath="library.json"):
        self.filepath = Path(filepath)
        self.titles: List[Title] = []

    def list_titles(self):
        return self.titles

    def _find_index_by_id(self, title_id: int):
        for i, t in enumerate(self.titles):
            if t.id == title_id:
                return i
        return None

    def _load_file(self):
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_file(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _refresh_titles_from_data(self, data):
        self.titles = [Title(**t) for t in data]

    def load(self):
        data = self._load_file()
        if data:
            self._refresh_titles_from_data(data)
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

        self.titles.append(title)
        data = [t.to_dict() for t in self.titles]
        self._save_file(data)

        return {"success": True, "count": len(self.titles), "title": title.to_dict()}

    def update_title(self, title_id: int, **kwargs):
        index = self._find_index_by_id(title_id)
        title_dict = self.titles[index].to_dict()

        for key, value in kwargs.items():
            title_dict[key] = value

        self.titles[index] = Title(**title_dict)
        data = [t.to_dict() for t in self.titles]
        self._save_file(data)

        return {"success": True, "title": self.titles[index].to_dict()}

    def delete_title(self, title_id: int):
        data = self._load_file()
        index = self._find_index_by_id(title_id)

        deleted_title = data.pop(index)
        self._save_file(data)
        self._refresh_titles_from_data(data)

        return {"success": True, "title": deleted_title}