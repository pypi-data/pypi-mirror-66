# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vsot', 'vsot.antlr']

package_data = \
{'': ['*']}

install_requires = \
['antlr4-python3-runtime==4.8', 'click>=7.0', 'pathspec>=0.8.0,<0.9.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6']}

entry_points = \
{'console_scripts': ['vsot = vsot.cli:main']}

setup_kwargs = {
    'name': 'vsot',
    'version': '0.1.4',
    'description': 'VSOT - Django/jinja template formatter',
    'long_description': '===================================================\nVSOT - Like black_, but for Django/Jinja2 templates\n===================================================\n\n\n.. image:: https://img.shields.io/pypi/v/vsot.svg\n        :target: https://pypi.python.org/pypi/vsot\n\n.. image:: https://img.shields.io/travis/benhowes/vsot.svg\n        :target: https://travis-ci.com/benhowes/vsot\n\n.. image:: https://img.shields.io/github/license/benhowes/vsot\n        :alt: License - MIT\n\nHTML Template formatter\n\nUse VSOT to automatically format your django templates. No need to manually reflow text or tags when you add/remove content.\n\nFree software: MIT license\n\n\nFeatures\n--------\n\n* Mimics black in terms of options and configuration.\n* Automatically supports all built in django/jinja2 tags\n* Safe - VSOT ensures that it does not change the meaning of the templates\n\n\nInstallation\n------------\n\n.. code-block:: console\n\n    pip install vsot\n\nDev Setup\n---------\n\nRequirements:\n- Python 3.6 or later\n- Docker\n- Python poetry (see `poetry docs`_)\n\n1. Clone repo\n\n2. Installation\n\n.. code-block:: console\n\n    poetry install\n\n\nCredits\n-------\n\n- A lot of the code for this was repurposed from black_\n- Antlr4_ is used for the parser, along with using the `HTML parser from the antlr library`_ as a starting point\n- This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n.. _black: https://github.com/psf/black\n.. _`poetry docs`: https://python-poetry.org/docs/#installation\n.. _Antlr4: https://github.com/antlr/antlr4\n.. _`HTML parser from the antlr library`: https://github.com/antlr/grammars-v4\n',
    'author': 'Ben Howes',
    'author_email': 'ben@ben-howes.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benhowes/vsot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
