from string import ascii_letters
from .models import User
import base64, hmac, hashlib


SECRET_KEY = "a05f2a0015e3b66bb740f1df1e60eef17e0d59f066fa4e1933a1387e475b7986"
PASSWORD_SALT = '768d6ff9470a6befffaade6d0419f4aed7ee0fc008ba7515be7f2bc76cba1b40'

def is_include_digit(passw: str) -> bool:
    for pas in passw:
        if pas.isdigit():
            return True
    else:
        return False

def is_include_all_register(passw: str) -> bool:
    Large = 0
    Small = 0
    for i in passw:
        if i.isupper():
            Large += 1
        if i.islower():
            Small += 1
    return Large > 0 and Small > 0


def is_include_only_latin(passw: str) -> bool:
    passw = passw.lower()
    for i in passw:
        if i.isalpha() and i not in ascii_letters:
            return False
    return True

def check_password_dictionary(passw: str) -> bool:
    with open('Authentication/easiest-passwords.txt', encoding='utf-8') as text:
        s = text.read()
    if passw in s:
        return False
    else:
        return True

def password_valid(self):
    password_repeat = self.cleaned_data['confirm_password']
    password = self.cleaned_data['password']
    if password != password_repeat:
        self._errors['confirm_password'] = self.error_class(["↕↕ The passwords don't match! ↕↕"])
        return False
    if len(password) <= 5 or len(password) >= 20:
        self._errors['password'] = self.error_class([" Password must be longer than 5 and less than 20 ↓ characters ↓"])
        return False
    if not is_include_digit(password):
        self._errors['password'] = self.error_class(["↓ The password must contain at least one digit ↓"])
        return False
    if not is_include_all_register(password):
        self._errors['password'] = self.error_class(["↓ Password must contain at least one upper and lower case character ↓"])
        return False
    if not is_include_only_latin(password):
        self._errors['password'] = self.error_class(["↓ Password must contain only the Latin alphabet ↓"])
        return False
    if not check_password_dictionary(password):
        self._errors['password'] = self.error_class(["↓ Your password is on the list of the easiest ↓"])
        return False
    return True

def check_bd_nick(self):
    nickname = self.cleaned_data['nickname']
    try:
        user = User.objects.get(nickname=nickname)
    except Exception:
        return True
    self._errors['nickname'] = self.error_class(
        ["↓ A user with this nickname is already registered ↓"])
    return False


def check_bd_email(self):
    email = self.cleaned_data['email']
    try:
        user = User.objects.get(email=email)
    except Exception:
        return True
    self._errors['email'] = self.error_class(
        ["↓ A user with this email is already registered ↓"])
    return False

def sign_data(data: str) -> str:
    """Возвращает подписанные данные"""
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()

def get_username_from_signed_string(username_singed: str):
    try:
        username_base64, sign = username_singed.split(".")
        username = base64.b64decode(username_base64.encode()).decode()
        valid_sign = sign_data(username)
        if hmac.compare_digest(valid_sign, sign):
            return username
    except Exception:
        return None

def verify_password(password: str, user: User) -> bool:

    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_password_hash=user.password.lower()
    return password_hash == stored_password_hash