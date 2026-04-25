# Virtual University Student Bot 🎓

A console-based chat simulator that acts as a knowledgeable virtual university student assistant.
Helps students manage deadlines, browse courses, and store their academic profile — all from the terminal.

## Features

| Command | Description |
|---|---|
| `start` | Show welcome screen and your profile |
| `help` | List all available commands |
| `profile` | Create or update your student profile |
| `deadlines` | Show all saved deadlines |
| `add deadline` | Add a new assignment deadline |
| `remove deadline` | Remove a deadline by number |
| `courses` | Browse available university courses |
| `search courses <kw>` | Search courses by keyword |
| `exit` | Exit the bot |

## Project Structure

```
vus_bot/
├── main.py              # Entry point & main command loop
├── handlers/            # Input routing — one file per command group
│   ├── start_handler.py
│   ├── help_handler.py
│   ├── profile_handler.py
│   ├── deadline_handler.py
│   └── course_handler.py
├── services/            # Business logic layer
│   ├── student_service.py
│   ├── deadline_service.py
│   ├── course_service.py
│   └── json_repository.py  # Shared JSON persistence base class
├── models/              # Data models (dataclasses)
│   └── student.py
├── tests/               # Unit tests (pytest)
│   ├── test_services.py
│   └── test_commands.py
└── data/                # Auto-created JSON storage (gitignored)
    ├── profile.json
    └── deadlines.json
```

## How to Run

```bash
python main.py
```

No external dependencies required — uses only the Python standard library.

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

Expected output: **41 passed**

## Code Quality

```bash
pip install black flake8
black .
flake8 .
```

Both tools should report no issues.

## Example Session

```
>> start
  Welcome to Virtual University Student Bot!

>> profile
  Your name       : Ruslan
  Your specialty  : CS-22-1
  Study year (1-6): 4
  Profile saved! Welcome, Ruslan.

>> add deadline
  Subject        : Math
  Task           : Homework 1
  Due date       : 2025-05-20
  Saved: [2025-05-20] Math — Homework 1

>> search courses python
  Machine Learning Fundamentals (4 credits) [available]
  Introduction to supervised and unsupervised ML with Python.

>> exit
  Goodbye! Good luck with your studies!
```

## Team

| # | Name | Role |
|---|---|---|
| 1 | Зима Руслан | Розробник (логіка) + Тимлід |
| 2 | Козловський Влад | Розробник (back-end) |
| 3 | Овчаренко Артем | Тестувальник (QA) |
