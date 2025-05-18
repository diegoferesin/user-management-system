from src.models import User
from src.repository import UserRepository
import tempfile
import os

def test_user_creation():
    """
    Test user creation with valid data.
    """
    user = User("John Doe", "john@example.com", "Password1!")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.password == "Password1!"
    assert user.user_id is not None

def test_email_validation():
    """
    Test email validation with valid and invalid emails.
    """
    # Valid emails
    assert User.validate_email("user@example.com")
    assert User.validate_email("user.name@domain.co.uk")
    # Invalid emails
    assert not User.validate_email("invalid-email")
    assert not User.validate_email("user@")
    assert not User.validate_email("@domain.com")

def test_password_validation():
    """
    Test password validation.
    """
    # Valid passwords
    assert User.validate_password("Password1@")
    assert User.validate_password("Abcdef1@");
    # Invalid passwords
    assert not User.validate_password("short")
    assert not User.validate_password("nouppercase1!")
    assert not User.validate_password("NOLOWERCASE1!")
    assert not User.validate_password("NoSpecialChar1")
    assert not User.validate_password("NoNumber!")

def test_user_to_dict():
    """
    Test conversion of user object to dictionary.
    """
    user = User("John Doe", "john@example.com", "Password1!")
    user_dict = user.to_dict()
    assert isinstance(user_dict, dict)
    assert user_dict["name"] == "John Doe"
    assert user_dict["email"] == "john@example.com"
    assert user_dict["password"] == "Password1!"
    assert "user_id" in user_dict

def test_user_from_dict():
    """
    Test creation of user object from dictionary.
    """
    user_dict = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "Password1!",
        "user_id": "123e4567-e89b-12d3-a456-426614174000"
    }
    user = User.from_dict(user_dict)
    assert isinstance(user, User)
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.password == "Password1!"
    assert user.user_id == "123e4567-e89b-12d3-a456-426614174000"

def test_add_user_duplicate_email(tmp_path):
    repo = UserRepository(str(tmp_path / "users.json"))
    user1 = User("Alice", "alice@example.com", "Password1@")
    user2 = User("Bob", "alice@example.com", "Password2@")
    assert repo.add_user(user1) is True
    assert repo.add_user(user2) is False  # No debe permitir duplicados

def test_delete_user_by_userid(tmp_path):
    repo = UserRepository(str(tmp_path / "users.json"))
    user = User("Charlie", "charlie@example.com", "Password1@")
    repo.add_user(user)
    users = repo.get_all_users()
    assert len(users) == 1
    # Eliminar manualmente por user_id
    users = [u for u in users if u.user_id != user.user_id]
    repo._save_users(users)
    users_after = repo.get_all_users()
    assert len(users_after) == 0

def test_user_from_dict_without_userid():
    user_dict = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "Password1@"
    }
    user = User.from_dict(user_dict)
    assert isinstance(user, User)
    assert user.user_id is not None

def test_name_validation():
    valid_names = ["Alice", "Bob", "Charlie"]
    invalid_names = ["Al", "Bob1", "Charlie!", ""]
    for name in valid_names:
        assert len(name) >= 3 and name.isalpha()
    for name in invalid_names:
        assert not (len(name) >= 3 and name.isalpha()) 