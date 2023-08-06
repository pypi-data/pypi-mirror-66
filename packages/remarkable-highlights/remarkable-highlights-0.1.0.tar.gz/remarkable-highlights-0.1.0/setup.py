# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['remarkable_highlights']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF>=1.16.17,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'descartes[debug]>=1.1.0,<2.0.0',
 'matplotlib[debug]>=3.2.1,<4.0.0',
 'shapely>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['remarkable-highlights = '
                     'remarkable_highlights.extract:main']}

setup_kwargs = {
    'name': 'remarkable-highlights',
    'version': '0.1.0',
    'description': 'Extract highlights from PDFs exported from the reMarkable web interface.',
    'long_description': None,
    'author': 'Ben Longo',
    'author_email': 'benlongo9807@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
