"""Hash and cryptografy functions.

    Helper on password and secrets security;
"""
import string
from hashlib import sha256
import secrets



ALPHABET = string.ascii_letters + string.digits

def get_hashed_password(password: str, salt: str):
    salted_password = password + salt
    return sha256(salted_password.encode()).hexdigest()


def create_salt(size: int = 8):
    salt = ''.join([secrets.choice(ALPHABET) for i in range(size)])
    return salt


