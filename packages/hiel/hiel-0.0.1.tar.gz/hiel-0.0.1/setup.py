# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hiel', 'hiel.services', 'hiel.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0', 'typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['hiel = hiel.cli:main']}

setup_kwargs = {
    'name': 'hiel',
    'version': '0.0.1',
    'description': 'a command line utility for bootstrapping projects with git',
    'long_description': '# Hiel\n\nA command line utility used to bootstrap projects without having to repeat the same processes over and over again.\n\n## Installation\n\nTo install `hiel` on your machine simply pull it from the internet (lol) using Pypi.\n\n```sh\npip install --user hiel\n```\n\n### Note\n\nHiel is somewhat customized for my local machine, so to make use of it ensure you have the following on your PC.\n\n* [Setup SSH for Github](https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account)\n\n* [Yarn](https://yarnpkg.com/) package manager is installed on your PC\n\n* You have at least [Python3.6](https://www.python.org/downloads/release/python-360/) installed on your PC\n\n* [Git](https://git-scm.com/) installed on your PC\n\nOnce this is done, get a personal access token from [Github](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) to ensure bootstrapped projects can be pushed to version control (Github). The access token is stored in `$HOME/.hiel` and can be updated anytime.\nYou don\'t need to create this file as it\'d be created automatically when you run `HIEL` for the first time.\n\n<!-- markdownlint-disable MD033 -->\n<div align="center">\n  <img src="https://github.com/BolajiOlajide/hiel/blob/master/token.png?raw=true" alt="github token" />\n</div>\n\n#### Commands\n\n* To view the help command\n\n```sh\nhiel --help\n```\n\n* Bootstrap a project\n\n```sh\nhiel <PROJECT_NAME> --type=[js|py] # type is used to specify the type of project, if its python/js\n```\n\n* To view the version of Hiel being used\n\n```sh\nhiel --version\n```\n',
    'author': 'Bolaji Olajide',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BolajiOlajide/hiel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.6.8',
}


setup(**setup_kwargs)
