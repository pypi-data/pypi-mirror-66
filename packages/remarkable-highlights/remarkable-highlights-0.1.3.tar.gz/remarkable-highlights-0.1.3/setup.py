# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['remarkable_highlights']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF>=1.16.17,<2.0.0', 'click>=7.1.1,<8.0.0', 'shapely>=1.7.0,<2.0.0']

extras_require = \
{'debug': ['matplotlib>=3.2.1,<4.0.0', 'descartes>=1.1.0,<2.0.0']}

entry_points = \
{'console_scripts': ['remarkable-highlights = '
                     'remarkable_highlights.extract:main']}

setup_kwargs = {
    'name': 'remarkable-highlights',
    'version': '0.1.3',
    'description': 'Extract highlights from PDFs exported from the reMarkable web interface.',
    'long_description': '# remarkable-highlights\n\nInspired and derived from https://github.com/soulisalmed/biff\n\nAutomatically extract highlights and clippings from PDFs annotated with your reMarkable.\n',
    'author': 'Ben Longo',
    'author_email': 'benlongo9807@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benlongo/remarkable-highlights',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
