from string import ascii_letters

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