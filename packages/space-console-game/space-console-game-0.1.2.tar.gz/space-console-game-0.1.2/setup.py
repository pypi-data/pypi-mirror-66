# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['space_console_game']

package_data = \
{'': ['*'], 'space_console_game': ['frames/*']}

entry_points = \
{'console_scripts': ['space-console-game = space_console_game.app:main']}

setup_kwargs = {
    'name': 'space-console-game',
    'version': '0.1.2',
    'description': 'We fly in space, we surf the Universe',
    'long_description': None,
    'author': 'velivir',
    'author_email': 'vitaliyantonoff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
