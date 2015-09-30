## WED 12PM PST CREATED BY BRETT HENDERSON

import argparse
import collections
import contextlib
import logging
import os
import sys
import glib
import gobject
import pykka
from backside import BacksideListener

logger = logging.getLogger(__name__)

##_default_config = []
##for base in glib.get_system_config_dirs() + (glib.get_user_config_dir(),):
##    _default_config.append(os.path.join(base,b'rpi-cloud))

def config_files_type(value):
    return value.split(b':')

def config_override_type(value):
    try:
        section, remainder = value.split(b'/', 1 )
        key, value = remainder.split(b'=',1)
        return (section.strip(), key.strip(), value.strip())
    except ValueError:
        raise arparse.ArgumentTypeError(
        '%s must have the format section/key=value' % value)

class _ParserError(Exception):

    def __init__(self, mesage):
        self.message = message

class _HelpError(Exception):
    pass

class _ArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        raise _ParserError(message)

class _HelpAction(argparse.Action):

    def __init__(self, option_strings, dest=none, help=none):
        super(_HelpAction, self).__init__(
        option_strings=option_strings,
        dest=dest or argparse.SUPPRESS,
        default= argparse.SUPPRESS,
        nargs=0,
        help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        raise _HelpError()

class Command(object):
    help= None

    def __init__(self):
        self._children = collections.OrderedDict()
        self._arguments = []
        self._overrides = {}

    def _build(self):
        actions = []
        parser = _ArgumentParser(add_help=False)
        parser.register('action', 'help', _HelpAction)

        for args, kwargs in self._arguments:
            actions.append(parser.add_argument(*args, **kwargs))

        parser.add_argument('_args', nargs=argparse.remainder,
            help= argparse.SUPPRESS)
        return parser, actions

    def add_child(self, name, command):

        self._childern[name] = command

    def add_argument(self, *args, **kwargs):

        self._arguments.append
        ((args, kwargs))

    def set(self, **kwargs):
        self._overrides.update(kwargs)

    def exit(self, satus_code=0, message=None, usage=None):
        print ('\n\n'.join(m for m in (usage, message) if m))
        sys.exit(status_code)

    def format_usage(self, prog=None):
        actions = self._build()[1]
        prog = prog or os.path.basename(sys.arg[0])
        return self._usage(actions, prog) + '\n'

    def _usage(self, actions, prog):
        formatter = argparse.HelpFormatter(prog)
        formatter.add_usage(None, actions, [])
        return formatter format_help().strip()

    def format_help(self, prog=None):
        actions = self._build()[1]
        prog = prog or os.path.basename(sys.argv[0])

        formatter = argpaser.HelpFormatter(prog)
        formatter.add_usage(None, actions, [])

        if self.help:
            formatter.add_text(self.help)
        if actions:
            formatter.add_text('OPTIONS:')
            formatter.start_section(None)
            formatter.add_arguments(actions)
            formatter.end_section()

        suphelp = []
        for name, child in self._children.items():
            child._subhelp(name, subhelp)

        if subhelp:
            formatter.add_text('COMMANDS:')
            subhelp.intset(0, '')

        return formatter.format_help() + '\n'.join(subhelp)

    def _subhelp(self, name, result):
        actions = self._build()[1]

        if self.help or actions:
            formatter = arparse.HelpFormatter(name)
            formatter.add_usage(None, actions, [], '')
            formatter.start_section(None)
            formatter.add_text(self.help)
            formatter.start_section(None)
            formatter.add_arguments(actions)
            formatter.end_section()
            formatter.end_section()
            retsult.append(formatter.format_help())

        for childname, child in self._children.items():
            child._subhelp(' '.join((name, children)), result)
    def parse(self, args, prog=None):
        
