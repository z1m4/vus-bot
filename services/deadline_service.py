"""Deadline service — business logic for managing assignment deadlines."""

import os
from typing import List

from models.student import Deadline
from services.json_repository import JsonRepository

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "deadlines.json")


def _validate_deadline(subject: str, task: str, due_date: str) -> None:
    """Validate deadline fields.

    Args:
        subject: Course or subject name — must not be blank.
        task: Assignment description — must not be blank.
        due_date: Due date string — must not be blank.

    Raises:
        ValueError: If any field is empty or whitespace-only.
    """
    if not subject.strip():
        raise ValueError("Subject cannot be empty.")
    if not task.strip():
        raise ValueError("Task description cannot be empty.")
    if not due_date.strip():
        raise ValueError("Due date cannot be empty.")


class DeadlineService(JsonRepository):
    """Manages student assignment deadlines, persisted to a JSON file."""

    def __init__(self) -> None:
        """Initialise the service and load existing deadlines from disk."""
        super().__init__(DATA_FILE)
        self._deadlines: List[Deadline] = self._load()

    def add_deadline(self, subject: str, task: str, due_date: str) -> Deadline:
        """Add and persist a new deadline entry.

        Args:
            subject: Name of the subject.
            task: Description of the assignment.
            due_date: Due date string (e.g. '2025-05-20').

        Returns:
            The newly created Deadline instance.

        Raises:
            ValueError: If any field is empty.
        """
        _validate_deadline(subject, task, due_date)
        deadline = Deadline(
            subject=subject.strip(),
            task=task.strip(),
            due_date=due_date.strip(),
        )
        self._deadlines.append(deadline)
        self._save([d.__dict__ for d in self._deadlines])
        return deadline

    def get_all(self) -> List[Deadline]:
        """Return all deadlines sorted by due date (ascending)."""
        return sorted(self._deadlines, key=lambda d: d.due_date)

    def remove_deadline(self, index: int) -> Deadline:
        """Remove and return a deadline by its 1-based list index.

        Args:
            index: 1-based position in the deadline list.

        Returns:
            The removed Deadline instance.

        Raises:
            ValueError: If the index is out of range.
        """
        if not (1 <= index <= len(self._deadlines)):
            raise ValueError(
                f"Invalid index. Choose between 1 and {len(self._deadlines)}."
            )
        removed = self._deadlines.pop(index - 1)
        self._save([d.__dict__ for d in self._deadlines])
        return removed

    def _load(self) -> List[Deadline]:
        """Load deadlines from disk and deserialise into Deadline objects."""
        data = self._load_raw()
        if not data:
            return []
        try:
            return [Deadline(**item) for item in data]
        except TypeError:
            return []
