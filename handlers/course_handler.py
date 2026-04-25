"""Handler for course browsing commands."""

from services.course_service import CourseService


def handle_courses(course_service: CourseService) -> None:
    """Display all available courses."""
    courses = course_service.get_available()
    print(f"\n  Available courses ({len(courses)} open for enrolment):")
    print("  " + "-" * 44)
    for i, course in enumerate(courses, 1):
        print(f"  {i}. {course}")
        print()


def handle_search_courses(course_service: CourseService, keyword: str) -> None:
    """Search and display courses matching the keyword."""
    try:
        results = course_service.search(keyword)
    except ValueError as err:
        print(f"\n  Error: {err}\n")
        return

    if not results:
        print(f"\n  No courses found for '{keyword}'.\n")
        return

    print(f"\n  Search results for '{keyword}' ({len(results)} found):")
    print("  " + "-" * 44)
    for course in results:
        print(f"  • {course}")
        print()
