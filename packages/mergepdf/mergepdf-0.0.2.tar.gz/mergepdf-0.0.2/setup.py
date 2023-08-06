# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mergepdf']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0']

entry_points = \
{'console_scripts': ['mergepdf = mergepdf:main']}

setup_kwargs = {
    'name': 'mergepdf',
    'version': '0.0.2',
    'description': '`mergepdf` is a package for merge PDF files.',
    'long_description': '`mergepdf` is a package for merge PDF files.\n::\n\n   $ mergepdf -h\n   usage: mergepdf [-h] [-i INPUT_DIR] [-o OUTPUT_FILE] [-k SORTED_KEY]\n   \n   Merge PDF files.\n   \n   optional arguments:\n     -h, --help            show this help message and exit\n     -i INPUT_DIR, --input-dir INPUT_DIR\n     -o OUTPUT_FILE, --output-file OUTPUT_FILE\n     -k SORTED_KEY, --sorted-key SORTED_KEY\n\nRequirements\n------------\n* Python 3.7 later\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install mergepdf\n\nHistory\n-------\n0.0.1 (2018-9-23)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/mergepdf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
