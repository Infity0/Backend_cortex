import re
from typing import Optional


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    return True, None


def validate_username(username: str) -> tuple[bool, Optional[str]]:

    if not username:
        return True, None 
    
    if len(username) < 2:
        return False, "Username must be at least 2 characters long"
    
    if len(username) > 100:
        return False, "Username must be at most 100 characters long"
    
    return True, None


def validate_prompt(prompt: str) -> tuple[bool, Optional[str]]:
 
    if len(prompt) < 3:
        return False, "Prompt must be at least 3 characters long"
    
    if len(prompt) > 500:
        return False, "Prompt must be at most 500 characters long"
    
    return True, None
