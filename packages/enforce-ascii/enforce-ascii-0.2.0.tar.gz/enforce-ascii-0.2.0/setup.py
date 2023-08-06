# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['enforce_ascii']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0.4,<4.0.0']

entry_points = \
{'console_scripts': ['enforce-ascii = enforce_ascii.__main__:main']}

setup_kwargs = {
    'name': 'enforce-ascii',
    'version': '0.2.0',
    'description': 'A pre-commit hook, that enforces ASCII content.',
    'long_description': "# Enforce ASCII\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n**VERSION**: `0.2.0`\n\nA Python package to find files containing non-ASCII encoded characters. If you\nfind any bugs, issues or anything, please use the [issue tracker][] on GitHub -\nissues and PRs are welcome ❤️\n\n## Install\n\nIt's on [PyPi] as `enforce-python`, you can install it with _pip_, _pipx_, etc.\n\n```shell\npip install enforce-ascii\n```\n\n## Usage\n\n```shell\n$ enforce-ascii --help\nusage: enforce-ascii [-h] [--version] [--check] FILENAME [FILENAME ...]\n\nA pre-commit hook, that rejects files containing non ASCII characters.\n\npositional arguments:\n  FILENAME    path to the files to check\n\noptional arguments:\n  -h, --help  show this help message and exit\n  --version   show program's version number and exit\n  --check     return code is `1`, when non-ASCII files are found\n```\n\n### Example\n\n```shell\n$ enforce-ascii tests/files/*/*.txt\n- tests/files/bad/special.txt (Windows-1252): there…\n- tests/files/bad/umlaut.txt (utf-8): föur, käle, Åir\n```\n\n## Pre-Commit\n\nThis can be used as a [pre-commit][] hook:\n\n```yaml\n- repo: https://github.com/brutus/enforce-ascii\n  rev: v0.2.0\n  hooks:\n      - id: enforce-ascii\n```\n\n[issue tracker]: https://github.com/brutus/enforce-ascii/issues\n[pre-commit]: https://pre-commit.com/\n[pypi]: https://pypi.org/project/enforce-ascii/\n",
    'author': 'Brutus',
    'author_email': 'brutus.dmc@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brutus/enforce-ascii/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
