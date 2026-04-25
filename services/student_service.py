"""Student service — business logic for profile management."""

import os
from typing import Optional

from models.student import Student
from services.json_repository import JsonRepository

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "profile.json")


def _validate_profile(name: str, specialty: str, year: int) -> None:
    """Validate student profile fields.

    Args:
        name: Student name — must not be blank.
        specialty: Academic programme — must not be blank.
        year: Study year — must be between 1 and 6 inclusive.

    Raises:
        ValueError: If any field fails validation.
    """
    if not name.strip():
        raise ValueError("Name cannot be empty.")
    if not specialty.strip():
        raise ValueError("Specialty cannot be empty.")
    if not (1 <= year <= 6):
        raise ValueError("Year must be between 1 and 6.")


class StudentService(JsonRepository):
    """Handles student profile storage and retrieval.

    Persists the profile as a JSON file so it survives bot restarts.
    """

    def __init__(self) -> None:
        """Initialise the service and load any existing profile from disk."""
        super().__init__(DATA_FILE)
        self._profile: Optional[Student] = self._load()

    def get_profile(self) -> Optional[Student]:
        """Return the current student profile, or None if not set."""
        return self._profile

    def create_profile(self, name: str, specialty: str, year: int) -> Student:
        """Create, persist, and return a new student profile.

        Args:
            name: Student's full name.
            specialty: Academic programme or specialty.
            year: Current study year (1–6).

        Returns:
            The newly created Student instance.

        Raises:
            ValueError: If any argument fails validation.
        """
        _validate_profile(name, specialty, year)
        self._profile = Student(
            name=name.strip(), specialty=specialty.strip(), year=year
        )
        self._save(self._profile.__dict__)
        return self._profile

    def clear_profile(self) -> None:
        """Delete the stored profile from memory and disk."""
        self._profile = None
        self._delete_file()

    def _load(self) -> Optional[Student]:
        """Load profile from disk and deserialise into a Student object."""
        data = self._load_raw()
        if data is None:
            return None
        try:
            return Student(**data)
        except TypeError:
            return None
