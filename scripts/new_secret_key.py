# -*- coding: utf-8 -*-
"""
Script to generate new Secret Key
"""
#
#   Imports
#
import random

import dotenv


#
#   Functions
#

def generate_random_secret_key():
    """ Generates a random Django SECRET_KEY """
    return ''.join(random.SystemRandom().
                   choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                   for _ in range(50))


def save_key(key):
    """ Save the given Key into the environment file """
    dotenv.set_key(dotenv.find_dotenv(), 'SECRET_KEY', key)


#
#   Entry Point
#

if __name__ == "__main__":
    new_key = generate_random_secret_key()
    save_key(new_key)
