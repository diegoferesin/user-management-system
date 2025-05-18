import re
import uuid
from typing import Dict, Optional

class User:
    """
    User model class that represents a user in the system.
    
    Attributes:
        user_id (str): Unique user identifier (UUID)
        name (str): User's full name
        email (str): User's email address
        password (str): User's password (stored as plain text for demo purposes)
    """
    
    def __init__(self, name: str, email: str, password: str, user_id: str = None):
        """
        Initialize a new User instance.
        
        Args:
            name (str): User's full name
            email (str): User's email address
            password (str): User's password
            user_id (str, optional): User's unique identifier (UUID). If not provided, a new UUID is generated.
        """
        self.user_id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate if the provided email contains an '@' and a valid domain part.
        Args:
            email (str): Email address to validate
        Returns:
            bool: True if email is valid, False otherwise
        """
        # Simple pattern: at least one character before and after '@', and a dot in the domain
        pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate if the password meets security requirements:
        - At least one digit
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one special character (@#$%^&+=)
        - No whitespace allowed
        - Minimum length of 8 characters
        
        Args:
            password (str): Password to validate
            
        Returns:
            bool: True if password is valid, False otherwise
        """
        pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,}$'
        return bool(re.match(pattern, password))
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convert user instance to dictionary format.
        
        Returns:
            Dict[str, str]: Dictionary containing user data
        """
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'User':
        """
        Create a User instance from a dictionary.
        
        Args:
            data (Dict[str, str]): Dictionary containing user data
            
        Returns:
            User: New User instance
        """
        return cls(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            user_id=data.get('user_id')
        ) 