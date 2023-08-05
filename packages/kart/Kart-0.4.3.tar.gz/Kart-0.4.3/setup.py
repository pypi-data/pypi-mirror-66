# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kart']

package_data = \
{'': ['*']}

install_requires = \
['feedgen>=0.9,<0.10',
 'jinja2>=2.11,<3.0',
 'livereload>=2.6,<3.0',
 'paka.cmark>=2.2,<3.0',
 'python-frontmatter>=0.5,<0.6',
 'pyyaml>=5.1,<6.0']

setup_kwargs = {
    'name': 'kart',
    'version': '0.4.3',
    'description': 'A very flexible static site generator written in python',
    'long_description': None,
    'author': 'Giacomo Caironi',
    'author_email': 'giacomo.caironi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
