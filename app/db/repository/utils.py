import random


def random_username(email: str):

    i = email.find("@")

    username = email[:i] + str(random.randint(1, 1000000))

    return username
