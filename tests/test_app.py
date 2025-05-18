from src.app import UserManagementApp
from src.models import User
import pytest

# Test de registro de usuario exitoso
def test_register_user_success(monkeypatch, tmp_path):
    app = UserManagementApp()
    app.repository.file_path = str(tmp_path / "users.json")
    # Simula entradas válidas para nombre, email y password
    inputs = iter(["Alice", "alice@example.com", "Password1@"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    app.register_user()
    users = app.repository.get_all_users()
    assert len(users) == 1
    assert users[0].name == "Alice"
    assert users[0].email == "alice@example.com"

# Test de búsqueda de usuario por email
def test_search_user_by_email(monkeypatch, tmp_path, capsys):
    app = UserManagementApp()
    app.repository.file_path = str(tmp_path / "users.json")
    user = User("Bob", "bob@example.com", "Password1@")
    app.repository.add_user(user)
    # Simula opción 1 (email) y el email a buscar
    inputs = iter(["1", "bob@example.com"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    app.search_users()
    captured = capsys.readouterr()
    assert "User found" in captured.out
    assert "bob@example.com" in captured.out

# Test de eliminación de usuario por UserID
def test_delete_user_by_userid(monkeypatch, tmp_path, capsys):
    app = UserManagementApp()
    app.repository.file_path = str(tmp_path / "users.json")
    user = User("Carol", "carol@example.com", "Password1@")
    app.repository.add_user(user)
    # Simula el user_id a eliminar
    inputs = iter([user.user_id])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    app.delete_user()
    users = app.repository.get_all_users()
    assert len(users) == 0
    captured = capsys.readouterr()
    assert "User deleted successfully" in captured.out 