# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subtitle_sync', 'subtitle_sync.utils']

package_data = \
{'': ['*']}

install_requires = \
['Scrapy>=2.0.1,<3.0.0',
 'spacy>=2.2.4,<3.0.0',
 'srt>=3.0.0,<4.0.0',
 'subliminal>=2.0.5,<3.0.0']

setup_kwargs = {
    'name': 'subtitle-sync',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'VVNoodle',
    'author_email': 'brickkace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
