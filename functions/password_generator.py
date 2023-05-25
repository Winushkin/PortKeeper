from random import choices
def generate_password():
    password = "".join(choices([chr(i) for i in range(ord("a"), ord("z"))] + list("1234567890"), k = 8))
    return password