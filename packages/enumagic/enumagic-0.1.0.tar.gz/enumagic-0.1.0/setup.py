# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enumagic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enumagic',
    'version': '0.1.0',
    'description': 'Enums infused with magic.',
    'long_description': 'enumagic\n========\n\nPython enums that work like magic.\n\n.. csv-table::\n   :align: center\n   :header-rows: 1\n   :widths: auto\n\n   Release, Usage, Tests, License\n   |pypi|, |rtfd|, |test|, |zlib|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/enumagic.svg?logo=python\n   :target: https://pypi.org/project/enumagic/\n   :alt: PyPI\n\n.. |rtfd| image:: https://img.shields.io/readthedocs/enumagic.svg?logo=read-the-docs\n   :target: https://enumagic.readthedocs.io/en/latest/\n   :alt: Read the Docs\n\n.. |test| image:: https://github.com/ObserverOfTime/enumagic.py/workflows/tests/badge.svg\n   :target: https://github.com/ObserverOfTime/enumagic.py/actions?query=workflow%3Atests\n   :alt: GitHub Actions\n\n.. |zlib| image:: https://img.shields.io/badge/license-zlib-blue.svg?logo=spdx\n   :target: https://spdx.org/licenses/Zlib.html#licenseText\n   :alt: Zlib License\n\n\n| The project is designed so that each module is self-sufficient.\n| You are free to vendor the one(s) you need into your project,\n| as long as you adhere to the terms of the Zlib license.\n',
    'author': 'ObserverOfTime',
    'author_email': 'chronobserver@disroot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ObserverOfTime/enumagic.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
