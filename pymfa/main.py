# -*- coding:utf-8 -*-
from __future__ import division, print_function, unicode_literals
from future_builtins import *
import os
import sys
import argparse
import ConfigParser
import pyotp
sys.path.append(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'vendor'))

INI_FILE_PATH = "~/.pymfa/config"
INI_FILE = (os.path.expanduser(INI_FILE_PATH))


def get_config(configfile):
    """
    get config from config file

    Args:
        configfile (str): value to config file path
    returns:
        RawConfigParser: RawConfigParser instance
    """
    config = ConfigParser.RawConfigParser()

    config.read(configfile)
    return config


def add_setting(profile, key, description):
    """
    Save setting to config file

    Args:
        profile (str) : Session name when saving configs
        key (str) : Value to save in the config file as option name key
        description : Value to save in the config file as option name description
    """

    config = get_config(INI_FILE)
    # The section name "DEFAULT" is a default section name,
    # and since it can not be confirmed by has_section,
    # it checks whether it is "DEFAULT" first
    if profile != 'DEFAULT':
        if not config.has_section(profile):
            config.add_section(profile)
    config.set(profile, 'key', key)
    config.set(profile, 'description', description)

    # Check existence of configuration file
    # If there is a directory, we can create a file
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(INI_FILE, 'wb') as configfile:
        config.write(configfile)
    print(get_totp(key), end="")


def get_totp(key):
    """
    Get a TOTP code at the current time

    Args:
        key (str): value to config file path
    returns:
        str: TOTP code (it is a 6 digit number)
    """
    totp = pyotp.TOTP(key)
    return totp.now()


def command_add(args):
    """
    Save the secret key.
    It is possible to include profiles and descriptions.

    Args:
        args (argparse): command arguments
    """
    add_setting(args.profile, args.key, args.description)


def command_get(args):
    """
    Display a TOTP code at the current time

    Args:
        args (argparse): command arguments

    """
    config = get_config(INI_FILE)
    key = config.get(args.profile, 'key')
    print(get_totp(key), end="")


def command_list(args):
    """
    Print a list of saved profile

    Args:
        args (argparse): command arguments
    """
    config = get_config(INI_FILE)
    if config.has_option('DEFAULT', 'key'):
        print_list(config, 'DEFAULT')
    for section in config.sections():
        print_list(config, section)


def print_list(config, section):
    """
    Reads the configuration and print it as formatted

    Args:
        config (RawConfigParser): RawConfigParser instance
        section (str): section name
    """
    if config.has_option(section, 'description'):
        print(section + " " + config.get(section, 'description'))
    else:
        print(section)


def command_help(args, parser):
    """
    Show command help

    Args:
        args (argparse): command arguments
        parser (ArgumentParser): ArgumentParser instnce
    """
    print(parser.parse_args([args.command, '--help']))


def main():
    """
    Create commands
    """
    parser = argparse.ArgumentParser(
        description='Manage TOTP tokens for multi-factor authentication')
    subparsers = parser.add_subparsers()

    parser.add_argument('-p', '--profile', type=str,
                        default="DEFAULT", help='Choice a acount')

    # set add subcommand
    parser_add = subparsers.add_parser('add', help='see `add -h`')
    parser_add.add_argument('key', help='Secret Key')
    parser_add.add_argument('-d', '--description',
                            type=str, default="", help='Key Description')
    parser_add.set_defaults(handler=command_add)

    # set list subcommand
    parser_commit = subparsers.add_parser('list', help='see `list -h`')
    parser_commit.set_defaults(handler=command_list)

    # set get subcommand
    parser_commit = subparsers.add_parser('get', help='see `get -h`')
    parser_commit.set_defaults(handler=command_get)

    # set help subcommand
    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument(
        'command', help='command name which help is shown')
    parser_help.set_defaults(handler=command_help)

    # Parse the command line argument
    # and execute the corresponding handler function
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        # help command requires a parser,
        # pass it when the help command is called
        if args.handler.__name__ == "command_help":
            args.handler(args, parser)
        else:
            args.handler(args)
    else:
        # Display help for unknown subcommand
        parser.print_help()
if __name__ == '__main__':
    main()
