"""
Virtual University Student Bot
Entry point — main command loop.
"""

from handlers.course_handler import handle_courses, handle_search_courses
from handlers.deadline_handler import (
    handle_add_deadline,
    handle_list_deadlines,
    handle_remove_deadline,
)
from handlers.help_handler import handle_help
from handlers.profile_handler import handle_profile
from handlers.start_handler import handle_start
from services.course_service import CourseService
from services.deadline_service import DeadlineService
from services.student_service import StudentService


def handle_command(
    command: str,
    student_service: StudentService,
    deadline_service: DeadlineService,
    course_service: CourseService,
) -> None:
    """Route a user command string to the appropriate handler.

    Args:
        command: Raw input string from the user.
        student_service: Injected StudentService instance.
        deadline_service: Injected DeadlineService instance.
        course_service: Injected CourseService instance.
    """
    cmd = command.strip().lower()

    if cmd == "start":
        handle_start(student_service)
    elif cmd == "help":
        handle_help()
    elif cmd == "profile":
        handle_profile(student_service)
    elif cmd == "deadlines":
        handle_list_deadlines(deadline_service)
    elif cmd == "add deadline":
        handle_add_deadline(deadline_service)
    elif cmd == "remove deadline":
        handle_remove_deadline(deadline_service)
    elif cmd == "courses":
        handle_courses(course_service)
    elif cmd.startswith("search courses "):
        keyword = command[len("search courses ") :].strip()  # noqa: E203
        handle_search_courses(course_service, keyword)
    elif cmd == "search courses":
        print("\n  Usage: search courses <keyword>  (e.g. search courses python)\n")
    else:
        print(f"\n  Unknown command: '{command}'. Type 'help' to see all commands.\n")


def main() -> None:
    """Initialise all services and start the main input loop."""
    student_service = StudentService()
    deadline_service = DeadlineService()
    course_service = CourseService()

    handle_start(student_service)

    while True:
        try:
            command = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye! Good luck with your studies!\n")
            break

        if not command:
            continue

        if command.lower() == "exit":
            print("\n  Goodbye! Good luck with your studies!\n")
            break

        handle_command(command, student_service, deadline_service, course_service)


if __name__ == "__main__":
    main()
