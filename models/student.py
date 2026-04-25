"""Data models for the Virtual University Student bot."""

from dataclasses import dataclass


@dataclass
class Student:
    """Represents a university student profile.

    Attributes:
        name: Full name of the student.
        specialty: Student's academic specialty or programme.
        year: Current year of study (1–6).
        language: Preferred interface language (default: 'en').
    """

    name: str
    specialty: str
    year: int
    language: str = "en"

    def __str__(self) -> str:
        """Return a human-readable summary of the student profile."""
        return f"{self.name} | {self.specialty} | Year {self.year}"


@dataclass
class Deadline:
    """Represents an assignment deadline.

    Attributes:
        subject: Name of the subject or course.
        task: Description of the assignment or task.
        due_date: Due date as a string (e.g. '2025-05-20').
    """

    subject: str
    task: str
    due_date: str

    def __str__(self) -> str:
        """Return a formatted deadline string."""
        return f"[{self.due_date}] {self.subject} — {self.task}"


@dataclass
class Course:
    """Represents an elective university course.

    Attributes:
        name: Full name of the course.
        credits: Number of ECTS credits.
        description: Short description of course content.
        available: Whether the course is open for enrolment.
    """

    name: str
    credits: int
    description: str
    available: bool = True

    def __str__(self) -> str:
        """Return a formatted course summary."""
        status = "available" if self.available else "full"
        return f"{self.name} ({self.credits} credits) [{status}]\n  {self.description}"
