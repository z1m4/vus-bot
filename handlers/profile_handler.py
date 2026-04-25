"""Handler for profile creation and display."""

from services.student_service import StudentService


def handle_profile(student_service: StudentService) -> None:
    """Show current profile or guide user through creation."""
    profile = student_service.get_profile()

    if profile:
        print("\n  Your current profile:")
        print(f"  Name      : {profile.name}")
        print(f"  Specialty : {profile.specialty}")
        print(f"  Year      : {profile.year}")
        answer = input("\n  Update profile? (yes/no): ").strip().lower()
        if answer not in ("yes", "y"):
            print()
            return

    print("\n  Let's set up your profile.")
    try:
        name = input("  Your name       : ").strip()
        specialty = input("  Your specialty  : ").strip()
        year_raw = input("  Study year (1-6): ").strip()

        if not year_raw.isdigit():
            print("  Error: year must be a number.\n")
            return

        profile = student_service.create_profile(name, specialty, int(year_raw))
        print(f"\n  Profile saved! Welcome, {profile.name}.\n")

    except ValueError as err:
        print(f"\n  Error: {err}\n")
