# -*- coding: utf-8 -*-
# @author: leesoar
# @email: secure@tom.com
# @email2: employ@aliyun.com

"""Curl To Lang

Thanks for curlconverter.
"""
import argparse
import os
import platform

import execjs

from curl2 import version

optional_title = 'optional arguments'


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super(CapitalisedHelpFormatter, self).__init__(prog,
                                                       indent_increment=2,
                                                       max_help_position=30,
                                                       width=200)
        self._action_max_length = 20

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

    class _Section(object):

        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()

            # return nothing if the section was empty
            if not item_help:  return ''

            # add the heading if the section was non-empty
            if self.heading is not argparse.SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                if self.heading == optional_title:
                    heading = '%*s\n%s:\n' % (current_indent, '', self.heading.title())
                else:
                    heading = '%*s%s:' % (current_indent, '', self.heading.title())
            else:
                heading = ''

            return join(['\n', heading, item_help])


ctx = execjs.compile(open(os.path.join(os.path.dirname(__file__), "curl.py")).read())

support_lang = ["go", "python", "node", "php", "r", "strest", "rust", "elixir", "dart", "json", "ansible", "matlab"]

parser = argparse.ArgumentParser(
    description=f"Curl convert to programming lang. Currently supports {', '.join(support_lang)}, etc.",
    prog="curl2", formatter_class=CapitalisedHelpFormatter,
    add_help=False)
parser.add_argument('-v', '--version', action='version', version=version(), help='Get version of curl2')
parser.add_argument('-h', '--help', action='help', help='Show help message')
parser.add_argument('-l', '--lang', default="python", type=str.lower, help="Set the output language, default is python")
parser.add_argument('-c', '--code', type=str, help="Curl code to parse")
curl_code = parser.parse_args().code
lang = parser.parse_args().lang


def run():
    try:
        if lang not in support_lang:
            return "Sorry, this lang is currently not supported."

        ret = ctx.call("curl", curl_code, lang).split("#NB.")[0]
        if "windows" in platform.system().lower():
            return "\n" + f"Output: {lang.capitalize().center(7)}".center(50).join(["=" * 52 + "\n=", "=\n" + "=" * 52]) + f"\n{ret}"
        return "\n" + f"\033[1;31;40mOutput: {lang.capitalize().center(7)}\033[0m".center(64).\
            join(["\033[1;32;40m=\033[0m" * 52 + "\n\033[1;32;40m=\033[0m", "\033[1;32;40m=\033[0m\n" +
                  "\033[1;32;40m=\033[0m" * 52]) + f"\n{ret}"
    except:
        return "\nError! Please check your curl code."
