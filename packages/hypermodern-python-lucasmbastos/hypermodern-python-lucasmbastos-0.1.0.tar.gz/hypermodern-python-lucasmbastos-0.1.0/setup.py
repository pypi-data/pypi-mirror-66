# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python_lucasmbastos']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.5.1,<4.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python-lucasmbastos = '
                     'hypermodern_python_lucasmbastos.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python-lucasmbastos',
    'version': '0.1.0',
    'description': 'The Hypermodern Python Project',
    'long_description': '# hypermodern-python-lucasmbastos\n\n![Tests](https://github.com/lucasmbastos/hypermodern-python-lucasmbastos/workflows/Tests/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/lucasmbastos/hypermodern-python-lucasmbastos/branch/master/graph/badge.svg)](https://codecov.io/gh/lucasmbastos/hypermodern-python-lucasmbastos)\n\nFollowing the https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769 tutorial series\n',
    'author': 'Lucas de Miranda',
    'author_email': 'lucasmbastos94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lucasmbastos/hypermodern-python-lucasmbastos',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
