# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vspoetry']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['vspoetry = vspoetry:main']}

setup_kwargs = {
    'name': 'vspoetry',
    'version': '0.1.0',
    'description': 'Automatically save the running poetry virtual environmment to your vscode settings.json',
    'long_description': '# VSpoetry\n\nSmall package that automate adding the Poetry virtual environment path to VScode settings.json so VScode can find the right environment for the project.\n\n',
    'author': 'MattiooFR',
    'author_email': 'dugue.mathieu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MattiooFR/vspoetry',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
