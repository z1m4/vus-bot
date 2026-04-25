"""Handler for deadline management commands."""

from services.deadline_service import DeadlineService


def handle_list_deadlines(deadline_service: DeadlineService) -> None:
    """Display all stored deadlines."""
    deadlines = deadline_service.get_all()
    if not deadlines:
        print("\n  No deadlines saved yet. Use 'add deadline' to add one.\n")
        return

    print(f"\n  Your deadlines ({len(deadlines)} total):")
    print("  " + "-" * 44)
    for i, d in enumerate(deadlines, 1):
        print(f"  {i}. {d}")
    print()


def handle_add_deadline(deadline_service: DeadlineService) -> None:
    """Prompt user for deadline details and save."""
    print("\n  Add a new deadline:")
    try:
        subject = input("  Subject        : ").strip()
        task = input("  Task           : ").strip()
        due_date = input("  Due date       : ").strip()

        deadline = deadline_service.add_deadline(subject, task, due_date)
        print(f"\n  Saved: {deadline}\n")

    except ValueError as err:
        print(f"\n  Error: {err}\n")


def handle_remove_deadline(deadline_service: DeadlineService) -> None:
    """Remove a deadline by its list number."""
    deadlines = deadline_service.get_all()
    if not deadlines:
        print("\n  No deadlines to remove.\n")
        return

    handle_list_deadlines(deadline_service)
    try:
        raw = input("  Enter number to remove: ").strip()
        if not raw.isdigit():
            print("  Error: please enter a valid number.\n")
            return
        removed = deadline_service.remove_deadline(int(raw))
        print(f"\n  Removed: {removed}\n")

    except ValueError as err:
        print(f"\n  Error: {err}\n")
