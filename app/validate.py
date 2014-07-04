"""
validity checking utility functions

each function will:
* check to see if they are valid input for that type or throw an AssertionError
* return a normalised version of the input
"""
import bcrypt
from app import app
from gettext import gettext as _
from validate_email import validate_email


class ValidationError(Exception):
    pass


def username(name):
    """
      check that the length > 3
    """
    if len(name) < 4:
        raise ValidationError(_('Username too short'))
    return name


def email(email):
    """
       use validate_email to verify format & dns
       normalise the domain part to lowercase
    """
    if '@' not in email:
        raise ValidationError(_('No @ sign in email address'))
    email = email.rsplit('@', 2)
    if len(email[1]) < 4:
        raise ValidationError(_('Email too short'))
    if '.' not in email[1]:
        raise ValidationError(_('No tld for email address?'))
    email = '@'.join([email[0], email[1].lower()])
    if not validate_email(email, verify=app.config['VERIFY_EMAIL_ADDRESSES']):
        raise ValidationError(_('Email address appears invalid'))
    return email


def password(password):
    """
       check that the password is longer than 6 characters
       "normalise" to bcrypt hash
    """
    if len(password) < 6:
        raise ValidationError(_('Password too short'))
    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, salt)
