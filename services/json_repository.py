"""Shared JSON persistence base — eliminates duplication across services."""

import json
import os


class JsonRepository:
    """Base class providing reusable JSON load/save logic.

    Subclasses pass their data file path to this constructor and then
    call _save(), _load_raw(), and _delete_file() instead of
    implementing file I/O themselves.

    Args:
        data_file: Absolute path to the JSON file used for persistence.
    """

    def __init__(self, data_file: str) -> None:
        """Initialise the repository with the given file path."""
        self._data_file = data_file

    def _save(self, data: object) -> None:
        """Serialise *data* to JSON and write it to disk.

        Creates the parent directory automatically if it does not exist.
        """
        os.makedirs(os.path.dirname(self._data_file), exist_ok=True)
        with open(self._data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load_raw(self) -> object:
        """Read and deserialise the JSON file.

        Returns:
            Parsed Python object, or None if the file does not exist or
            contains invalid JSON.
        """
        if not os.path.exists(self._data_file):
            return None
        try:
            with open(self._data_file, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, TypeError):
            return None

    def _delete_file(self) -> None:
        """Remove the backing JSON file if it exists."""
        if os.path.exists(self._data_file):
            os.remove(self._data_file)
