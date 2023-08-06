# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['addpage']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'pdfformfiller>=0.4,<0.5', 'reportlab>=3.5.42,<4.0.0']

entry_points = \
{'console_scripts': ['addpage = addpage:main']}

setup_kwargs = {
    'name': 'addpage',
    'version': '0.0.3',
    'description': '`addpage` is a package for adding page number to PDF file.',
    'long_description': '`addpage` is a package for adding page number to PDF file.\n::\n\n   $ addpage -h\n   usage: addpage [-h] [-o OUTFILE] [-n FONT_NAME] [-z FONT_SIZE] [-s START]\n                  [-k SKIP] [-x MARGIN_X] [-y MARGIN_Y]\n                  [-a {center,left,right}] [-f FORMAT]\n                  infile\n   \n   Add page number to PDF file.\n   \n   positional arguments:\n     infile                input PDF file\n   \n   optional arguments:\n     -h, --help            show this help message and exit\n     -o OUTFILE, --outfile OUTFILE\n     -n FONT_NAME, --font-name FONT_NAME\n     -z FONT_SIZE, --font-size FONT_SIZE\n     -s START, --start START\n     -k SKIP, --skip SKIP\n     -x MARGIN_X, --margin-x MARGIN_X\n     -y MARGIN_Y, --margin-y MARGIN_Y\n     -a {center,left,right}, --alignment {center,left,right}\n     -f FORMAT, --format FORMAT\n\n\nRequirements\n------------\n* Python 3.6 later\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install addpage\n\nHistory\n-------\n0.0.1 (2018-9-23)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/jcal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
