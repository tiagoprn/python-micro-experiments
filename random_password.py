# coding: utf-8

"""
Demonstrate the use of the click library for CLI arguments.

Must have the following installed through pip:
    $ pip install click

Run examples:

    $ python click_cli_arguments.py  --help

    $ touch /tmp/test.txt && python click_cli_arguments.py --file-name '/tmp/test.txt' --technique 'random' --random-number 99;

"""

import os
import string
import sys

from random import choice

import click

allowed_symbols = '!#*+,-/?@^_~'

@click.command()
@click.option('--num_chars', help='How many chars.', type=int, required=True)
def run(num_chars):
    print(f'Will generate a password with {num_chars} characters.')

    allowed_chars = string.ascii_letters + allowed_symbols + string.digits
    password = "".join(choice(allowed_chars) for x in range(num_chars))

    print(f'Your password is: {password}')


if __name__ == "__main__":
    run()
