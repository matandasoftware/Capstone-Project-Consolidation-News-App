# Task Manager Application

A professional task management system built with Python that allows users to register, create, manage, and track tasks with comprehensive reporting capabilities.

## Features

- User authentication and registration
- Task creation and assignment
- Task editing and completion tracking
- Admin-only features (user registration, task deletion, statistics)
- Comprehensive reporting (task overview, user overview)
- Overdue task detection
- PEP 8 compliant code

## Project Structure

```
capstone project task 3/
│
├── main.py                  # Entry point of the application
├── data_access.py          # Data access layer (repositories)
├── business_logic.py        # Business logic (services, Task class)
├── user_interface.py        # UI layer (menus, user input)
├── utilities.py            # Utility functions (date validation, etc.)
├── config.py               # Configuration settings
├── constants.py            # Application constants
│
├── tests/
│   ├── __init__.py         # Tests package init
│   └── tests.py            # Unit tests
│
├── user.txt                # User data storage
├── tasks.txt               # Task data storage
├── task_overview.txt       # Generated task report
├── user_overview.txt       # Generated user report
│
├── .flake8                 # Flake8 linting configuration
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Installation

1. **Clone or download the project**

2. **Create a virtual environment**
   ```bash
   python -m venv myenv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

4. **Install dependencies** (if any)
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

### Default Credentials
- Username: `admin`
- Password: `adm1n`

### Menu Options

**Admin Menu:**
- `r` - Register new user
- `a` - Add task
- `va` - View all tasks
- `vm` - View my tasks
- `vc` - View completed tasks
- `del` - Delete tasks
- `ds` - Display statistics
- `gr` - Generate reports
- `e` - Exit

**User Menu:**
- `a` - Add task
- `va` - View all tasks
- `vm` - View my tasks
- `e` - Exit

## Running Tests

Run the unit tests:
```bash
python -m unittest tests.tests
```

Or run tests with verbose output:
```bash
python -m unittest tests.tests -v
```

## Linting

Check code for PEP 8 compliance:
```bash
flake8 *.py
```

## Development

### Adding Dependencies

After installing a new package:
```bash
pip freeze > requirements.txt
```

### Code Style

This project follows PEP 8 guidelines. Use Flake8 for linting:
```bash
pip install flake8
flake8 *.py
```

## Architecture

The application follows a layered architecture:

1. **User Interface Layer** (`user_interface.py`)
   - Handles user input/output
   - Menu navigation
   - Display formatting

2. **Business Logic Layer** (`business_logic.py`)
   - Service classes (UserService, TaskService, ReportService)
   - Business rules and validation
   - Task class definition

3. **Data Access Layer** (`data_access.py`)
   - Repository pattern implementation
   - File I/O operations
   - Data persistence

4. **Utilities** (`utilities.py`)
   - Helper functions
   - Date validation and formatting

5. **Configuration** (`config.py`, `constants.py`)
   - Application settings
   - Constants and menu definitions

## Testing

The test suite covers:
- Task creation and manipulation
- User authentication and registration
- Task filtering and statistics
- Date validation utilities

Tests use mocking to avoid file system dependencies.

## License

This project is for educational purposes.

## Author

Created as part of the Python for Software Engineering coursework.
