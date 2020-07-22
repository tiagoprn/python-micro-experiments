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
import sys

import click

SAMPLING_TECHNIQUES = ['random', 'first', 'last']


@click.command()
@click.option('--file-name', help='The input file name.')
@click.option('--technique',
              type=click.Choice(SAMPLING_TECHNIQUES),
              help=('The technique to apply '
                    'the sampling on the file: ('
                    '{})'.format(', '.join(SAMPLING_TECHNIQUES))))
@click.option('--random-number',
              help=('For the technique "random_lines_number", '
                    'specify the number of records you want on the sample.'),
              default=50)
def run(file_name, technique, random_number):
    if not file_name:
        print 'Parameter "--file-name" is required.'
        sys.exit(1)

    if not os.path.exists(file_name):
        print 'The file "{}" does not exist on the filesystem.'.format(
            file_name)
        sys.exit(1)

    message = ['The values this script will use are: ',
               'FILE_NAME: {}'.format(file_name),
               'TECHNIQUE: {}'.format(technique),
               'RANDOM_NUMBER: {}'.format(random_number)]

    print '\n'.join(message)

if __name__ == "__main__":
    run()
