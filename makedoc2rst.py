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

import datetime
import re
import rst


class makedoc2rst():
    """ Convert c source file with makedoc markup to rst markup file
    c_file: c source file containing block comments (/* */) at the beginning
    rst_file: destination file with rst markup
    """
    def __init__(self, c_file, rst_file):
        self.c_file = c_file
        self.rst_file = rst_file

    def convert(self):
        """ Implementation of converting c file to rst file """
        rst_str = ''
        with open(self.c_file, 'r') as c_file:
            # Get comments inside of /* */
            comments = self._extract_comments(c_file.read())
            if comments == "":
                print("Cannot find Newlib style comments in {f}".format(f=self.c_file))
                return ''

            # Parse comments
            command_text_list = []
            command_text_list.extend(self._insert_comment_block(self.c_file))
            command_text_list.extend(self._extract_command_and_text(comments))
            command_text_list.extend(self._append_origin_block())

            # Process text based on command type
            for command, text in command_text_list:
                transformed_command = rst.transform_command(command)
                transformed_text = rst.transform_text(command, text)
                rst_str += rst.get_command_processor(command)(
                    transformed_command, transformed_text
                )

        with open(self.rst_file, 'w') as rst_file:
            rst_file.write(rst_str)
        return rst_str

    def _is_command(self, s):
        """
        A command is a single word of at least 3 characters, all uppercase
        :param s: input string
        :return: True if s is a single command, otherwise False
        """
        return True if re.match('^[A-Z_]{3,}\s*$', s) else False

    def _extract_comments(self, content):
        """
        Extract content inside of /* */
        :param content: input file content
        :return: extracted comments
        """
        comments = ''
        comments_match = re.search('/\*\nFUNCTION(\*(?!/)|[^*])*\*/', content)
        if comments_match:
            wrapped_comments = comments_match.group()
            comments = wrapped_comments.lstrip('/*').rstrip('*/').lstrip().rstrip()
        return comments

    def _extract_command_and_text(self, comments):
        """
        Extract command and text from input string content
        :param comments: input string containing command and text
        :return: a list containing (command, text) tuple
        """
        command = ''
        text = ''
        command_text_list = []
        for line in comments.splitlines():
            if self._is_command(line):
                if command and text:
                    command_text_list.append((command, text))
                command = line.rstrip()
                text = ''
            else:
                text += line + '\n'
        return command_text_list

    def _insert_comment_block(self, c_file):
        """
        Insert C source file name and date info to the RST file
        :param command_text_list: original command_text_list
        :return: command_text_list with custom comment block
        """
        return [
            ('COMMENT', 'This file was automatically generated from the file:'),
            ('COMMENT', c_file),
            ('COMMENT', 'Generated on: {date}'.format(
                date=datetime.datetime.today().strftime('%Y-%m-%d'),
            ),
            ),
        ]

    def _append_origin_block(self):
        origin = (
            'The information in this section was generated from '
            'documentation included with the `Newlib C Library '
            '<https://sourceware.org/newlib/>`_.'
        )
        return [('ORIGIN', origin)]

