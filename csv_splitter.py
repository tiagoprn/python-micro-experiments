# coding: utf-8

"""
Split a text (CSV) file into multiple files, keeping the header.

For it to work, you must install "click":

    $ pip install click
"""

import os
import sys

import click

OUTPUT_FOLDER = 'splitted'


def _add_line_to_file(file_name, line):
    with open(file_name, 'a') as output_file:
        output_file.write(line)


def _get_and_create_output_folder(original_file_name):
    root_folder = os.path.dirname(original_file_name)
    full_output_folder = os.path.join(root_folder, OUTPUT_FOLDER)
    if not os.path.exists(full_output_folder):
        os.makedirs(full_output_folder)
    return full_output_folder


def _get_current_file_name(original_file_name, files_count):
    full_output_folder = _get_and_create_output_folder(original_file_name)
    current_output_file_name = os.path.join(
        full_output_folder,
        '{}.{}'.format(os.path.basename(original_file_name),
                       str(files_count).zfill(3)))
    return current_output_file_name


@click.command()
@click.option('--file-name', help='file name. E.g.: "tmp/file.txt".')
@click.option('--maximum-lines-per-file',
              help='The maximum number of lines per file',
              default=500000)
def run(file_name, maximum_lines_per_file):
    print 'Starting...'

    if not os.path.exists(file_name):
        message = ('Input file "{}" does not exist. '
                   'I will exit now().\n'.format(file_name))
        print message
        sys.exit(-1)

    if not isinstance(maximum_lines_per_file, int):
        message = '--maximum-lines-per-file must be an integer.'
        print message
        sys.exit(-1)

    files_count = 1
    lines_counter = 0
    file_header = ''

    current_output_file_name = _get_current_file_name(file_name, files_count)

    with open(file_name, 'r') as input_file:
        for line in input_file.readlines():
            lines_counter += 1
            if lines_counter == 1:
                file_header = line
                if os.path.exists(current_output_file_name):
                    os.unlink(current_output_file_name)
            elif lines_counter == maximum_lines_per_file:
                files_count += 1
                lines_counter = 1
                current_output_file_name = _get_current_file_name(
                    file_name, files_count)
                if os.path.exists(current_output_file_name):
                    os.unlink(current_output_file_name)
                _add_line_to_file(current_output_file_name, file_header)
            _add_line_to_file(current_output_file_name, line)

    print 'Finished. The files are here: {}'.format(
        os.path.dirname(current_output_file_name))

if __name__ == '__main__':
    run()
