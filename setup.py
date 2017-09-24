# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from pymfa import __author__, __version__, __license__
 
setup(
        name             = 'pymfa',
        version          = __version__,
        description      = 'Manage TOTP tokens for multi-factor authentication',
        license          = __license__,
        author           = __author__,
        author_email     = '',
        url              = '',
        keywords         = 'mfa totp',
        packages         = find_packages(),
        install_requires = ['pyotp'],
        entry_points     = {
                                "console_scripts": [
                                    "pymfa=pymfa.main:main",
                                ],
                            },
        )