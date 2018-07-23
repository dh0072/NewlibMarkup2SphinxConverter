#!/usr/bin/env python
#
# RTEMS Tools Project (http://www.rtems.org/)
# Copyright 2018 Danxue Huang (danxue.huang@gmail.com)
# All rights reserved.
#
# This file is part of the RTEMS Tools package in 'rtems-tools'.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#


import argparse
import re
import rst


def is_command(s):
    """
    A command is a single word of at least 3 characters, all uppercase
    :param s: input string
    :return: True if s is a single command, otherwise False
    """
    return True if re.match('^[A-Z_]{3,}\s*$', s) else False


def extract_comments(content):
    """
    Extract content inside of /* */
    :param content: input file content
    :return: extracted comments
    """
    comments = ''
    comments_match = re.match('/\*(\*(?!/)|[^*])*\*/', content)
    if comments_match:
        wrapped_comments = comments_match.group()
        comments = wrapped_comments.lstrip('/*').rstrip('*/').lstrip().rstrip()
    return comments


def extract_command_and_text(content):
    """
    Extract command and text from input string content
    :param content: input string containing command and text
    :return: a tuple containing command and text
    """
    command = ''
    text = ''
    command_text_dict = {}
    for line in content.splitlines():
        if is_command(line):
            if command and text:
                command_text_dict[command] = text
            command = line.rstrip()
            text = ''
        else:
            text += line + '\n'
    return command_text_dict


def generate_rst(command_text_dict):
    rst_str = ''
    for command, text in command_text_dict.items():
        rst_str += rst.get_command_processor(command)(command, text)
    return rst_str


def get_parser():
    parser = argparse.ArgumentParser(
        description='Convert newlib style markup to rst markup'
    )
    parser.add_argument(
        '-s',
        '--source_file_dir',
        type=str,
        help='Source file directory with newlib style comments',
    )
    parser.add_argument(
        '-d',
        '--dest_file_dir',
        type=str,
        help='Destination directory for converted rst markup file',
    )
    return parser


def main(source_file_dir, dest_file_dir):
    with open(source_file_dir, 'r') as source_file, open(dest_file_dir, 'w') as dest_file:
        file_content = source_file.read()

        # Get comments inside of /* */
        comments = extract_comments(file_content)

        # Parse comments
        command_text_dict = extract_command_and_text(comments)

        # Process text based on command type
        rst_str = generate_rst(command_text_dict)

        dest_file.write(rst_str)


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.source_file_dir, args.dest_file_dir)
