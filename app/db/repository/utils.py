import random


def random_username(email:str):
    username = email[:6] + str(random.randint(1,1000000))
    
    return username
