import os
from colorama import Fore, Style

def clear_screen() -> None:
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str) -> None:
    """
    Print a formatted header.
    Args:
        title (str): Header title to display
    """
    print(f"\n{Fore.CYAN}{'=' * 50}")
    print(f"{title.center(50)}")
    print(f"{'=' * 50}{Style.RESET_ALL}\n")

def get_user_input(prompt: str) -> str:
    """
    Get user input with a formatted prompt.
    Args:
        prompt (str): Input prompt to display
    Returns:
        str: User input
    """
    return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")

def retry_input(prompt: str, validate_fn, error_msg: str, max_attempts: int = 4) -> str:
    """
    Prompt the user for input, validating with validate_fn, allowing up to max_attempts.
    Args:
        prompt (str): The prompt to display
        validate_fn (Callable[[str], bool]): Function to validate input
        error_msg (str): Error message to display on invalid input
        max_attempts (int): Maximum number of attempts
    Returns:
        str: Validated user input
    Raises:
        ValueError: If the user fails to provide valid input in max_attempts
    """
    attempts = 0
    while attempts < max_attempts:
        value = get_user_input(f"{prompt} [Attempts left: {max_attempts - attempts}]: ")
        if validate_fn(value):
            return value
        else:
            attempts += 1
            print(f"{Fore.RED}{error_msg} Attempts left: {max_attempts - attempts}{Style.RESET_ALL}")
    raise ValueError(error_msg) 