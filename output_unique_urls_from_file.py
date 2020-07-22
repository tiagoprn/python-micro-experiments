# coding: utf-8

"""
Given an input file with a list of urls, output another with deduplicated urls.

Must have the following installed through pip:
    $ pip install click

Run examples:

    $ python output_unique_urls_from_file.py  --help

    $ python output_unique_urls_from_file.py --file-name '/tmp/test.txt'
"""

import os
import sys

import click


@click.command()
@click.option('--file-name', help='The input file name.')
def run(file_name):
    if not file_name:
        print('Parameter "--file-name" is required.')
        sys.exit(1)

    if not os.path.exists(file_name):
        print('The file "{}" does not exist on the filesystem.'.format(
            file_name))
        sys.exit(1)

    output_file = "{}.uniques".format(file_name)

    print('Reading input file...')

    with open(file_name, 'r') as input:
        lines = input.readlines()

    print('Computing the unique urls list...')

    uniques = sorted(list(set(lines)))

    print('Writing the computed list to '
          'the output file {}...'.format(output_file))

    with open(output_file, 'w') as output:
        output.write(''.join(uniques))

    print('Finished. The output file is at: {}'.format(output_file))

if __name__ == "__main__":
    run()
