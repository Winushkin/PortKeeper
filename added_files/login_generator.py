from added_files.translator import translator
from random import randint


def generate_login(name: str) -> str:
    surname = name.split()[0]
    first_name = name.split()[1]
    login = translator(surname) + translator(first_name[0]) + str(randint(1, 19))
    return login

