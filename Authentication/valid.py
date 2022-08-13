from string import ascii_letters


class Registration:
    def __init__(self, log, passw):
        self.login = log
        self.password = passw

    @staticmethod
    def check_mail(log: str):
        if '.' in log[log.find('@'):]:
            return True
        else:
            return False

    @staticmethod
    def is_include_digit(passw: str) -> bool:
        for pas in passw:
            if pas.isdigit():
                return True
        else:
            return False

    @staticmethod
    def is_include_all_register(passw: str) -> bool:
        Large = 0
        Small = 0
        for i in passw:
            if i.isupper():
                Large += 1
            if i.islower():
                Small += 1
        return Large > 0 and Small > 0

    @staticmethod
    def is_include_only_latin(passw: str) -> bool:
        passw = passw.lower()
        for i in passw:
            if i.isalpha() and i not in ascii_letters:
                return False
        return True

    @staticmethod
    def check_password_dictionary(passw: str) -> bool:
        with open('easy_passwords.txt', encoding='utf-8') as text:
            s = text.read()
        if passw in s:
            return False
        else:
            return True

    @property
    def login(self):
        return self.__login

    @property
    def password(self):
        return self.__password

    @login.setter
    def login(self, log):
        if log.count('@') != 1:
            raise ValueError("Логин должен содержать один символ '@'")
        if not Registration.check_mail(log):
            raise ValueError("Логин должен содержать символ '.'")
        self.__login = log

    @password.setter
    def password(self, passw):
        if not isinstance(passw, str):
            raise TypeError("Пароль должен быть строкой")
        if len(passw) <= 4 or len(passw) >= 12:
            raise ValueError('Пароль должен быть длиннее 4 и меньше 12 символов')
        if not Registration.is_include_digit(passw):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not Registration.is_include_all_register(passw):
            raise ValueError('Пароль должен содержать хотя бы один символ верхнего и нижнего регистра')
        if not Registration.is_include_only_latin(passw):
            raise ValueError('Пароль должен содержать только латинский алфавит')
        if not Registration.check_password_dictionary(passw):
            raise ValueError('Ваш пароль содержится в списке самых легких')
        self.__password = passw