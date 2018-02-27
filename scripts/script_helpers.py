# -*- coding: utf-8 -*-
"""
Helper functions for Scripts
"""
#
#   Imports
#
import os

import click
import dotenv


#
#   Load env
#

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)


#
#   Functions
#

def get_env_var(variable):
    """Gets the given Variable or None"""
    return os.environ.get(variable)


def set_env_variables(dict_variables):
    """Sets the given Variables to the Environment"""
    for k, v in dict_variables.items():
        dotenv.set_key(dotenv_path, k, v)


def prompt(key, default_value, hide_input=False):
    """Prompts user for input"""
    text = key

    curr_value = default_value if get_env_var(key) is None else get_env_var(key)

    if curr_value is not None:
        if hide_input:
            text += " [" + ("*" * len(curr_value)) + "]"

    user_in = click.prompt(text, default=curr_value, hide_input=hide_input, confirmation_prompt=hide_input,
                           show_default=(not hide_input))

    return user_in


def process_input_dictionary(input_dict):
    """Process a dictionary specifying the data needed"""
    update_dict = dict()
    for k, (v, hide) in input_dict.items():
        user_in = prompt(k, v, hide)
        update_dict[k] = user_in
    set_env_variables(update_dict)
