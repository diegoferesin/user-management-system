import json
import os
from typing import List, Optional
from .models import User

class UserRepository:
    """
    Repository class for handling user data persistence.
    
    This class manages the storage and retrieval of user data using JSON files.
    """
    
    def __init__(self, file_path: str = "data/users.json"):
        """
        Initialize the UserRepository.
        
        Args:
            file_path (str): Path to the JSON file for storing user data
        """
        self.file_path = file_path
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """
        Ensure the data directory exists.
        Creates the directory if it doesn't exist.
        """
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            self._save_users([])
    
    def _load_users(self) -> List[User]:
        """
        Load users from the JSON file.
        
        Returns:
            List[User]: List of User objects
        """
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return [User.from_dict(user_data) for user_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_users(self, users: List[User]) -> None:
        """
        Save users to the JSON file.
        
        Args:
            users (List[User]): List of User objects to save
        """
        with open(self.file_path, 'w') as f:
            json.dump([user.to_dict() for user in users], f, indent=4)
    
    def add_user(self, user: User) -> bool:
        """
        Add a new user to the repository.
        
        Args:
            user (User): User object to add
            
        Returns:
            bool: True if user was added successfully, False if email already exists
        """
        users = self._load_users()
        if any(u.email == user.email for u in users):
            return False
        users.append(user)
        self._save_users(users)
        return True
    
    def get_all_users(self) -> List[User]:
        """
        Get all users from the repository.
        
        Returns:
            List[User]: List of all User objects
        """
        return self._load_users()
    
    def find_by_name(self, name: str) -> List[User]:
        """
        Find users by name (case-insensitive partial match).
        
        Args:
            name (str): Name to search for
            
        Returns:
            List[User]: List of matching User objects
        """
        users = self._load_users()
        name_lower = name.lower()
        return [user for user in users if name_lower in user.name.lower()]
    
    def delete_user(self, email: str) -> bool:
        """
        Delete a user by email.
        
        Args:
            email (str): Email of the user to delete
            
        Returns:
            bool: True if user was deleted, False if user not found
        """
        users = self._load_users()
        initial_length = len(users)
        users = [user for user in users if user.email != email]
        if len(users) < initial_length:
            self._save_users(users)
            return True
        return False 