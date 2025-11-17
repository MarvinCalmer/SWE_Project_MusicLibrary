from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .title import Title


class AbstractLibrary(ABC):
    """
    Abstract base class that defines the required interface for
    library implementations. Any subclass must implement all
    public methods for managing and accessing titles.
    """

    @abstractmethod
    def get_titles(self) -> List[Title]:
        """Return a list of all titles."""

    @abstractmethod
    def get_titles_by_id(self, index: int) -> Title:
        """Return a single title by index."""

    @abstractmethod
    def search_library(self, **kwargs) -> Dict[str, Any]:
        """Search for titles matching the given filters."""

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load titles from storage."""

    @abstractmethod
    def add_title(self, title: Title) -> Dict[str, Any]:
        """Add a new title to the library."""

    @abstractmethod
    def update_title(self, title_id: int, **kwargs) -> Dict[str, Any]:
        """Update an existing title."""

    @abstractmethod
    def delete_title(self, title_id: int) -> Dict[str, Any]:
        """Delete a title by ID."""
