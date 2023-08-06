# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bibtexgen']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.0,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.45.0,<5.0.0']

entry_points = \
{'console_scripts': ['bibtexgen = bibtexgen.entry:main']}

setup_kwargs = {
    'name': 'bibtexgen',
    'version': '0.0.1',
    'description': 'A tool to quickly export all references to bibtex',
    'long_description': None,
    'author': 'Shrey Dabhi',
    'author_email': 'shrey.dabhi23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdabhi23/bibtexgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
