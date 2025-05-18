import os
from typing import Optional
from colorama import init, Fore, Style
from decouple import config
from .models import User
from .repository import UserRepository
from .utils import clear_screen, print_header, get_user_input, retry_input

class UserManagementApp:
    """
    Main application class for user management system.
    
    This class provides a console-based interface for managing users.
    """
    
    def __init__(self):
        """
        Initialize the UserManagementApp.
        Sets up the repository and initializes colorama for colored output.
        """
        init()  # Initialize colorama
        self.repository = UserRepository(config('DATA_FILE_PATH', default='data/users.json'))
    
    def clear_screen(self) -> None:
        pass  # Now handled by utils.clear_screen
    
    def print_header(self, title: str) -> None:
        pass  # Now handled by utils.print_header
    
    def get_user_input(self, prompt: str) -> str:
        pass  # Now handled by utils.get_user_input
    
    def register_user(self) -> None:
        """
        Register a new user with input validation.
        """
        while True:
            print_header("Register New User")
            # Validar nombre antes de avanzar (4 intentos)
            try:
                name = retry_input(
                    "Enter name (only letters, min 3 chars)",
                    lambda n: len(n) >= 3 and n.isalpha(),
                    "Name must be at least 3 characters and only letters!"
                )
            except ValueError:
                print(f"{Fore.RED}User could not be registered: too many invalid name attempts. Returning to main menu.{Style.RESET_ALL}")
                return

            # Validar email antes de avanzar (4 intentos)
            def email_validator(email):
                if not User.validate_email(email):
                    return False
                if any(u.email == email for u in self.repository.get_all_users()):
                    return False
                return True
            try:
                email = retry_input(
                    "Enter email (e.g. user@example.com)",
                    email_validator,
                    "Invalid or already used email! Example: user@example.com"
                )
            except ValueError:
                print(f"{Fore.RED}User could not be registered: too many invalid email attempts. Returning to main menu.{Style.RESET_ALL}")
                return

            # Pedir password con condiciones y hasta 4 intentos
            password_conditions = (
                "Password requirements:\n"
                "- At least 8 characters\n"
                "- At least one digit\n"
                "- At least one lowercase letter\n"
                "- At least one uppercase letter\n"
                "- At least one special character (@#$%^&+=)\n"
                "- No whitespace allowed"
            )
            try:
                password = retry_input(
                    f"Enter password:\n{password_conditions}\nPassword:",
                    User.validate_password,
                    "Password does not meet requirements!"
                )
            except ValueError:
                print(f"{Fore.RED}User could not be registered: password was invalid 4 times. Returning to main menu.{Style.RESET_ALL}")
                return

            user = User(name, email, password)
            print(f"{Fore.GREEN}User registered successfully!{Style.RESET_ALL}")
            self.repository.add_user(user)
            break
    
    def list_users(self) -> None:
        """
        Display all registered users.
        """
        print_header("Registered Users")
        users = self.repository.get_all_users()
        
        if not users:
            print(f"{Fore.YELLOW}No users registered yet.{Style.RESET_ALL}")
            return
        
        for user in users:
            print(f"{Fore.CYAN}UserID: {user.user_id}")
            print(f"Name: {user.name}")
            print(f"Email: {user.email}{Style.RESET_ALL}")
            print("-" * 30)
    
    def search_users(self) -> None:
        """
        Search for a user by email or by UserID.
        """
        print_header("Search User")
        print("1. Search by Email")
        print("2. Search by UserID")
        option = get_user_input("Select an option (1-2): ")
        users = self.repository.get_all_users()
        if option == "1":
            email = get_user_input("Enter email to search: ")
            found = False
            for user in users:
                if user.email == email:
                    print(f"{Fore.GREEN}User found:{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}UserID: {user.user_id}")
                    print(f"Name: {user.name}")
                    print(f"Email: {user.email}{Style.RESET_ALL}")
                    found = True
                    break
            if not found:
                print(f"{Fore.YELLOW}No user found with that email.{Style.RESET_ALL}")
        elif option == "2":
            user_id = get_user_input("Enter UserID to search: ")
            found = False
            for user in users:
                if user.user_id == user_id:
                    print(f"{Fore.GREEN}User found:{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}UserID: {user.user_id}")
                    print(f"Name: {user.name}")
                    print(f"Email: {user.email}{Style.RESET_ALL}")
                    found = True
                    break
            if not found:
                print(f"{Fore.YELLOW}No user found with that UserID.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid option!{Style.RESET_ALL}")
    
    def delete_user(self) -> None:
        """
        Delete a user by UserID.
        """
        print_header("Delete User")
        user_id = get_user_input("Enter UserID of user to delete: ")
        users = self.repository.get_all_users()
        found = False
        for user in users:
            if user.user_id == user_id:
                users.remove(user)
                self.repository._save_users(users)
                print(f"{Fore.GREEN}User deleted successfully!{Style.RESET_ALL}")
                found = True
                break
        if not found:
            print(f"{Fore.RED}User not found!{Style.RESET_ALL}")
    
    def run(self) -> None:
        """
        Run the main application loop.
        """
        while True:
            clear_screen()
            print_header("User Management System")
            print(f"{Fore.CYAN}1. Register User")
            print("2. List Users")
            print("3. Search Users")
            print("4. Delete User")
            print(f"5. Exit{Style.RESET_ALL}")
            
            choice = get_user_input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.list_users()
            elif choice == "3":
                self.search_users()
            elif choice == "4":
                self.delete_user()
            elif choice == "5":
                print(f"\n{Fore.GREEN}Thank you for using the User Management System!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    app = UserManagementApp()
    app.run() 