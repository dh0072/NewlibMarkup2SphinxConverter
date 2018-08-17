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


import re


def register_processor_command():
    return {
        'FUNCTION': gen_function_summary,
        'SYNOPSIS': gen_code_block,
        'ANSI_SYNOPSIS': gen_code_block,
        'TRAD_SYNOPSIS': gen_code_block,
        'TYPEDEF': gen_code_block,
        'DESCRIPTION': gen_custom_directives,
        'INDEX': gen_custom_directives,
        'RETURNS': gen_custom_directives,
        'PORTABILITY': gen_custom_directives,
        'NOTES': gen_custom_directives,
        'ERRORS': gen_custom_directives,
        'BUGS': gen_custom_directives,
        'WARNINGS': gen_custom_directives,
        'QUICKREF': gen_nothing,
        'MATHREF': gen_nothing,
        'NEWPAGE': gen_nothing,
        'START': gen_nothing,
        'END': gen_nothing,
        'SEEALSO': gen_custom_directives,
    }


def get_command_processor(command):
    command_processor_dict = register_processor_command()
    if command in command_processor_dict:
        return command_processor_dict[command]
    else:
        print('Command {c} is not recognized, skip it'.format(c=command))
        return gen_nothing


def gen_function_summary(command, text):
    function_name = extract_function_name(text)
    summary = extract_summary(text)

    title = '.. {f}:\n\n{f} - {s}\n'.format(
        f=function_name,
        s=summary.capitalize()
    )
    dashes = '-' * len(text) + '\n'
    func_name_index = '.. index:: {name}\n'.format(name=function_name)
    summary_index = '.. index:: {summary}\n\n'.format(summary=summary)
    return title + dashes + func_name_index + summary_index


def extract_function_name(text):
    function_name = ''
    function_name_match = re.match('\s+(<<(>(?!>)|[^>])*>>)', text)
    if function_name_match:
        function_name = function_name_match.group(1).lstrip('<<').rstrip('>>')
    return function_name


def extract_summary(text):
    return text.split('---')[-1].rstrip()


def gen_code_block(command, text):
    return '**{c}:**\n\n.. code-block:: c\n\n{t}\n\n'.format(c = command, t=text)


def gen_nothing(command, text):
    return '\n\n'


def gen_custom_directives(command, text):
    return '**{c}:**\n\n{t}\n\n'.format(c=command, t=text)
