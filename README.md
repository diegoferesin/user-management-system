# User Management System

A Python-based user management system that provides a console interface for managing users. The system allows you to register, list, search, and delete users, with data persistence using JSON files.

## Features

- User registration with validation
- List all registered users
- Search users by name
- Delete users
- Data persistence using JSON files
- Colored console interface
- Environment variable configuration
- Input validation and error handling

## Requirements

- Python 3.10+
- Virtual environment (venv)
- Required packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following content:
```
DATA_FILE_PATH=data/users.json
```

## Usage

Run the application:
```bash
python3 -m src.app
```

### Example of valid passwords
- Example1: Abcdef1@
- Example2: StrongPass9#
- Example3: My$ecurePwd2

### Example of invalid passwords
- abcdefg (no uppercase, no digit, no special character)
- ABCDEFG1 (no lowercase, no special character)
- Abcdefgh (no digit, no special character)

The application provides a menu-driven interface with the following options:
1. Register User
2. List Users
3. Search User (by Email or UserID)
4. Delete User
5. Exit

When selecting option 3, you can choose to search for a user either by their email or by their UserID (UUID).

## Project Structure

```
user-management-system/
├── data/               # Data directory for JSON files
├── src/               # Source code
│   ├── __init__.py
│   ├── app.py         # Main application (console flow, menu)
│   ├── models.py      # User model and validation
│   ├── repository.py  # Data persistence
│   └── utils.py       # Reusable utilities (screen, input, headers, retry logic)
├── tests/             # Test files
├── .env              # Environment variables
├── requirements.txt  # Project dependencies
└── README.md        # This file
```

## Development

The project follows a modular structure:
- `models.py`: Contains the User class with validation methods
- `repository.py`: Handles data persistence using JSON files
- `utils.py`: Provides reusable utilities for input, screen clearing, headers, and retry logic for user input
- `app.py`: Provides the console interface and main application logic, using the utilities from `utils.py`

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Registration attempts and validation
- The user has up to 4 attempts to enter a valid name, email, and password.
- For each failed attempt, the system shows how many attempts are left.
- If the user fails 4 times in any field, an error is shown and the registration is cancelled, returning to the main menu. 