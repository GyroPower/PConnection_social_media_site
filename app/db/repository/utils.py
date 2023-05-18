import random


def random_username(email: str):

    i = email.find("@")

    username = email[:i] + str(random.randint(1, 1000000))

    return username


def see_image_type(filename: str):

    i = filename.find(".")

    image_type = filename[i:]

    print(image_type)

    return image_type
