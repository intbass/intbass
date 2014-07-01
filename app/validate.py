"""
validity checking utility functions

each function will:
* check to see if they are valid input for that type or throw an AssertionError
* return a normalised version of the input
"""
import bcrypt
from app import app
from validate_email import validate_email


def username(name):
    """
      check that the length > 3
    """
    assert len(name) > 3
    return name


def email(email):
    """
       use validate_email to verify format & dns
       normalise the domain part to lowercase
    """
    assert validate_email(email, verify=app.config['VERIFY_EMAIL_ADDRESSES'])
    email = email.rsplit('@', 2)
    email = '@'.join([email[0], email[1].lower()])
    return email


def password(password):
    """
       check that the password is longer than 6 characters
       "normalise" to bcrypt hash
    """
    assert len(password) > 6
    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, salt)
