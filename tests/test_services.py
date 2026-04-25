"""Unit tests for business logic services."""

import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.deadline_service import DeadlineService
from services.student_service import StudentService
from services.course_service import CourseService


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


class TestStudentService:
    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.service = build_student_svc(self.tmp)

    def test_create_profile_success(self):
        p = self.service.create_profile("Ruslan", "CS", 2)
        assert p.name == "Ruslan"
        assert p.specialty == "CS"
        assert p.year == 2

    def test_create_profile_empty_name_raises(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            self.service.create_profile("   ", "CS", 2)

    def test_create_profile_empty_specialty_raises(self):
        with pytest.raises(ValueError, match="Specialty cannot be empty"):
            self.service.create_profile("Ruslan", "  ", 2)

    def test_create_profile_year_too_low_raises(self):
        with pytest.raises(ValueError, match="Year must be between 1 and 6"):
            self.service.create_profile("Ruslan", "CS", 0)

    def test_create_profile_year_too_high_raises(self):
        with pytest.raises(ValueError, match="Year must be between 1 and 6"):
            self.service.create_profile("Ruslan", "CS", 7)

    def test_get_profile_none_when_empty(self):
        assert self.service.get_profile() is None

    def test_get_profile_after_create(self):
        self.service.create_profile("Vlad", "IT", 3)
        assert self.service.get_profile().name == "Vlad"

    def test_create_profile_strips_whitespace(self):
        p = self.service.create_profile("  Anna  ", "  Math  ", 1)
        assert p.name == "Anna"
        assert p.specialty == "Math"

    def test_clear_profile(self):
        self.service.create_profile("Ruslan", "CS", 2)
        self.service.clear_profile()
        assert self.service.get_profile() is None

    def test_overwrite_profile(self):
        self.service.create_profile("Ruslan", "CS", 2)
        self.service.create_profile("Vlad", "IT", 3)
        assert self.service.get_profile().name == "Vlad"


class TestDeadlineService:
    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.service = build_deadline_svc(self.tmp)

    def test_add_deadline_success(self):
        d = self.service.add_deadline("Math", "HW1", "2025-05-20")
        assert d.subject == "Math"
        assert d.task == "HW1"
        assert d.due_date == "2025-05-20"

    def test_add_empty_subject_raises(self):
        with pytest.raises(ValueError, match="Subject cannot be empty"):
            self.service.add_deadline("", "Task", "2025-05-01")

    def test_add_empty_task_raises(self):
        with pytest.raises(ValueError, match="Task description cannot be empty"):
            self.service.add_deadline("Math", "  ", "2025-05-01")

    def test_add_empty_date_raises(self):
        with pytest.raises(ValueError, match="Due date cannot be empty"):
            self.service.add_deadline("Math", "Task", "")

    def test_get_all_sorted_by_date(self):
        self.service.add_deadline("B", "t", "2025-06-01")
        self.service.add_deadline("A", "t", "2025-04-01")
        deadlines = self.service.get_all()
        assert deadlines[0].subject == "A"
        assert deadlines[1].subject == "B"

    def test_get_all_empty(self):
        assert self.service.get_all() == []

    def test_remove_success(self):
        self.service.add_deadline("Math", "HW1", "2025-05-01")
        self.service.add_deadline("Physics", "Lab", "2025-05-10")
        removed = self.service.remove_deadline(1)
        assert removed.subject == "Math"
        assert len(self.service._deadlines) == 1

    def test_remove_invalid_index_raises(self):
        self.service.add_deadline("Math", "HW1", "2025-05-01")
        with pytest.raises(ValueError, match="Invalid index"):
            self.service.remove_deadline(99)

    def test_remove_zero_index_raises(self):
        self.service.add_deadline("Math", "HW1", "2025-05-01")
        with pytest.raises(ValueError, match="Invalid index"):
            self.service.remove_deadline(0)

    def test_add_multiple(self):
        self.service.add_deadline("Math", "HW1", "2025-05-01")
        self.service.add_deadline("CS", "Project", "2025-05-15")
        self.service.add_deadline("English", "Essay", "2025-06-01")
        assert len(self.service.get_all()) == 3


class TestCourseService:
    def setup_method(self):
        self.service = CourseService()

    def test_get_all_count(self):
        assert len(self.service.get_all()) == 10

    def test_get_available_all_open(self):
        available = self.service.get_available()
        assert all(c.available for c in available)
        assert len(available) == 9

    def test_search_by_name(self):
        results = self.service.search("python")
        assert len(results) >= 1

    def test_search_by_description(self):
        results = self.service.search("SQL")
        assert len(results) >= 1

    def test_search_empty_raises(self):
        with pytest.raises(ValueError, match="Search keyword cannot be empty"):
            self.service.search("   ")

    def test_search_no_match(self):
        assert self.service.search("zzznomatch999") == []

    def test_search_case_insensitive(self):
        assert len(self.service.search("python")) == len(self.service.search("PYTHON"))

    def test_get_by_index_valid(self):
        c = self.service.get_by_index(1)
        assert c is not None
        assert c.name == "Algorithms & Data Structures"

    def test_get_by_index_out_of_range(self):
        assert self.service.get_by_index(999) is None

    def test_get_by_index_zero(self):
        assert self.service.get_by_index(0) is None
