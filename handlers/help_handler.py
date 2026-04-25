"""Handler for the /help command."""

COMMANDS = [
    ("start", "Show welcome message and your profile"),
    ("help", "Show this list of commands"),
    ("profile", "Create or view your student profile"),
    ("deadlines", "List all your upcoming deadlines"),
    ("add deadline", "Add a new deadline  (e.g. add deadline)"),
    ("remove deadline", "Remove a deadline by number"),
    ("courses", "Browse available university courses"),
    ("search courses <kw>", "Search courses by keyword"),
    ("exit", "Exit the bot"),
]


def handle_help() -> None:
    """Print all available commands with descriptions."""
    print("\n" + "-" * 50)
    print("  Available commands:")
    print("-" * 50)
    for cmd, desc in COMMANDS:
        print(f"  {cmd:<25} {desc}")
    print("-" * 50)
    print()
