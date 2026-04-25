"""Course service — business logic for browsing available university courses."""

from typing import List, Optional

from models.student import Course

# Static course catalogue (in a real system this would come from a DB/API)
_CATALOGUE: List[Course] = [
    Course(
        "Algorithms & Data Structures",
        5,
        "Core CS course covering sorting, graphs and dynamic programming.",
    ),
    Course(
        "Machine Learning Fundamentals",
        4,
        "Introduction to supervised and unsupervised ML with Python.",
    ),
    Course(
        "Web Development with Django",
        3,
        "Build full-stack web applications using the Django framework.",
    ),
    Course(
        "Database Systems",
        4,
        "Relational databases, SQL, indexing and query optimisation.",
    ),
    Course(
        "Computer Networks",
        3,
        "OSI model, TCP/IP, routing protocols and network security basics.",
    ),
    Course(
        "Software Engineering",
        4,
        "SDLC, Agile, design patterns and code quality practices.",
    ),
    Course(
        "Mobile Development (Flutter)",
        3,
        "Cross-platform mobile apps with Dart and Flutter.",
        available=False,
    ),
    Course(
        "Cybersecurity Essentials",
        3,
        "Threat models, cryptography, ethical hacking introduction.",
    ),
    Course(
        "Cloud Computing (AWS/GCP)",
        3,
        "Cloud architecture, serverless functions and containerisation.",
    ),
    Course(
        "Technical English for IT",
        2,
        "Academic writing, presentations and IT vocabulary.",
    ),
]


class CourseService:
    """Provides access to the university course catalogue."""

    def get_all(self) -> List[Course]:
        """Return all courses (available and unavailable)."""
        return list(_CATALOGUE)

    def get_available(self) -> List[Course]:
        """Return only courses currently open for enrolment."""
        return [c for c in _CATALOGUE if c.available]

    def search(self, keyword: str) -> List[Course]:
        """Search courses by keyword in name or description.

        Args:
            keyword: Search term (case-insensitive).

        Returns:
            List of matching Course objects.

        Raises:
            ValueError: If keyword is empty or whitespace-only.
        """
        if not keyword.strip():
            raise ValueError("Search keyword cannot be empty.")
        kw = keyword.lower()
        return [
            c for c in _CATALOGUE if kw in c.name.lower() or kw in c.description.lower()
        ]

    def get_by_index(self, index: int) -> Optional[Course]:
        """Return a course by its 1-based catalogue index.

        Args:
            index: 1-based position in the catalogue.

        Returns:
            The Course at that position, or None if out of range.
        """
        if not (1 <= index <= len(_CATALOGUE)):
            return None
        return _CATALOGUE[index - 1]
