# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['estimium']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'estimium',
    'version': '0.1.1',
    'description': "A collection of ML tools written with professor's chalk",
    'long_description': '<h1 align="center">Professor Estimium</h1>\n\n<p align="center">\n    <img src="https://raw.githubusercontent.com/mrtovsky/estimium/master/docs/images/professor-estimium.png" alt="Professor Estimium" class="center">\n</p>\n\n<h2 align="center">A collection of ML tools written with professor\'s chalk</h2>\n\n<p align="center">\n    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>\n    <a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit" style="max-width:100%;"></a>\n</p>\n\n<!-- prettier-ignore -->\n> _Application of these estimators is left as an exercise for the reader_ - Professor Estimium\n\n**Professor Estimium** is a **Python** package implementing frequently used\nfunctionalities to reduce writing Machine Learning boilerplates to a minimum.\n\nThe professor was guided by the principle that:\n\n<!-- prettier-ignore -->\n> _If you did something once, you did it enough times._\n',
    'author': 'Mateusz Zakrzewski',
    'author_email': 'mrtovsky@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
