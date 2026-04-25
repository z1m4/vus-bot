"""Unit tests for models and edge cases."""

import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.student import Course, Deadline, Student
from services.course_service import CourseService
from services.deadline_service import DeadlineService
from services.student_service import StudentService


def build_student_svc(tmp_dir):
    svc = StudentService.__new__(StudentService)
    svc._data_file = os.path.join(tmp_dir, "profile.json")
    svc._profile = None
    return svc


def build_deadline_svc(tmp_dir):
    svc = DeadlineService.__new__(DeadlineService)
    svc._data_file = os.path.join(tmp_dir, "deadlines.json")
    svc._deadlines = []
    return svc


class TestModels:
    def test_student_str(self):
        s = Student(name="Ruslan", specialty="CS", year=2)
        assert "Ruslan" in str(s)
        assert "CS" in str(s)
        assert "2" in str(s)

    def test_deadline_str(self):
        d = Deadline(subject="Math", task="HW1", due_date="2025-05-01")
        assert "Math" in str(d)
        assert "HW1" in str(d)
        assert "2025-05-01" in str(d)

    def test_course_str_available(self):
        c = Course("CS101", 3, "Intro to CS", available=True)
        assert "available" in str(c)

    def test_course_str_unavailable(self):
        c = Course("CS101", 3, "Intro to CS", available=False)
        assert "full" in str(c)

    def test_course_default_available(self):
        c = Course("CS101", 3, "Intro to CS")
        assert c.available is True


class TestEdgeCases:
    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.student_svc = build_student_svc(self.tmp)
        self.deadline_svc = build_deadline_svc(self.tmp)
        self.course_svc = CourseService()

    def test_profile_year_boundary_min(self):
        p = self.student_svc.create_profile("A", "CS", 1)
        assert p.year == 1

    def test_profile_year_boundary_max(self):
        p = self.student_svc.create_profile("A", "CS", 6)
        assert p.year == 6

    def test_remove_from_empty_raises(self):
        with pytest.raises(ValueError):
            self.deadline_svc.remove_deadline(1)

    def test_deadline_count_after_add_and_remove(self):
        self.deadline_svc.add_deadline("Math", "HW1", "2025-05-01")
        self.deadline_svc.add_deadline("CS", "Project", "2025-06-01")
        self.deadline_svc.remove_deadline(1)
        assert len(self.deadline_svc.get_all()) == 1

    def test_search_single_character(self):
        results = self.course_svc.search("a")
        assert isinstance(results, list)

    def test_multiple_profiles_overwrite(self):
        self.student_svc.create_profile("Ruslan", "CS", 2)
        self.student_svc.create_profile("Vlad", "IT", 3)
        assert self.student_svc.get_profile().name == "Vlad"
