# -*- coding:utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vendor'))
import argparse
import ConfigParser

import pyotp
from datetime import datetime, timedelta

INI_FILE_PATH="~/.pymfa/config"
INI_FILE = (os.path.expanduser(INI_FILE_PATH))
def get_config():
    config = ConfigParser.RawConfigParser()
    
    config.read(INI_FILE)
    return config

def add_setting(profile,key):
    config = get_config()
    if profile != 'DEFAULT' :
        if not config.has_section(profile) :
            config.add_section(profile)
    config.set(profile, 'key', key)
    
    # 設定ファイルの存在確認
    # ディレクトリがあれば、ファイルは作れる
    dir,_ =  os.path.split(INI_FILE)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(INI_FILE, 'wb') as configfile:
        config.write(configfile)
    print(get_totp(key), end="")

def get_totp(key):
    totp = pyotp.TOTP(key)
    return totp.now()

def command_add(args):
    add_setting(args.profile,args.key)

def command_get(args):
    config = get_config()
    key = config.get(args.profile,'key')
    print(get_totp(key), end="")
    
def command_list(args):
    config = get_config()
    if config.has_option('DEFAULT','key'):
        print('DEFAULT')
    for section in config.sections():
        print(section)
    
def command_help(args):
    print(parser.parse_args([args.command, '--help']))    

def main():
    parser = argparse.ArgumentParser(description='Manage TOTP tokens for multi-factor authentication')
    subparsers = parser.add_subparsers()

    #文字列オプション
    parser.add_argument('-p','--profile', type=str, default="DEFAULT", help='Choice a acount')


    # add コマンドの parser を作成
    parser_add = subparsers.add_parser('add', help='see `add -h`')
    parser_add.add_argument('key', help='Secret Key')
    parser_add.set_defaults(handler=command_add)

    # list コマンドの parser を作成
    parser_commit = subparsers.add_parser('list', help='see `list -h`')
    parser_commit.set_defaults(handler=command_list)

    # get コマンドの parser を作成
    parser_commit = subparsers.add_parser('get', help='see `get -h`')
    parser_commit.set_defaults(handler=command_get)

    # help コマンドの parser を作成
    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument('command', help='command name which help is shown')
    parser_help.set_defaults(handler=command_help)

    # コマンドライン引数をパースして対応するハンドラ関数を実行
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()
if __name__ == '__main__':
    main()