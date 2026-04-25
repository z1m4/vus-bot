"""Handler for the /start command."""

from services.student_service import StudentService


def handle_start(student_service: StudentService) -> None:
    """Welcome the user and show existing profile if available."""
    print("\n" + "=" * 50)
    print("  Welcome to Virtual University Student Bot!")
    print("=" * 50)

    profile = student_service.get_profile()
    if profile:
        print(f"\n  Hello again, {profile.name}!")
        print(f"  Specialty : {profile.specialty}")
        print(f"  Year      : {profile.year}")
    else:
        print("\n  No profile found. Use 'profile' to set up yours.")

    print("\n  Type 'help' to see all available commands.")
    print()
