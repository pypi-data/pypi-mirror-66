# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyuninstaller']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pyinstaller>=3.6,<4.0', 'uncompyle6>=3.6.6,<4.0.0']

entry_points = \
{'console_scripts': ['pyuninstaller = pyuninstaller.__main__:main']}

setup_kwargs = {
    'name': 'pyuninstaller',
    'version': '0.0.1',
    'description': 'Decompile what pyinstaller creates.',
    'long_description': 'pyuninstaller\n#############\n\n.. image:: https://travis-ci.org/supakeen/pyuninstaller.svg?branch=master\n    :target: https://travis-ci.org/supakeen/pyuninstaller\n\n.. image:: https://readthedocs.org/projects/pyuninstaller/badge/?version=latest\n    :target: https://pyuninstaller.readthedocs.io/en/latest/\n\n.. image:: https://pyuninstaller.readthedocs.io/en/latest/_static/license.svg\n    :target: https://github.com/supakeen/pyuninstaller/blob/master/LICENSE\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://img.shields.io/pypi/v/pyuninstaller\n    :target: https://pypi.org/project/pyuninstaller\n\n.. image:: https://codecov.io/gh/supakeen/pyuninstaller/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/supakeen/pyuninstaller\n\nAbout\n=====\n\n``pyuninstaller`` is Python pastebin software that tried to keep it simple but got\na little more complex.\n\nPrerequisites\n=============\n* Python >= 3.6\n* click\n* pyinstaller\n* uncompyle6\n',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supakeen/pyuninstaller',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
