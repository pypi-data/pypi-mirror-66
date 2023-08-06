# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toml_sort']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0', 'tomlkit>=0.5.8']

entry_points = \
{'console_scripts': ['toml-sort = toml_sort.cli:cli']}

setup_kwargs = {
    'name': 'toml-sort',
    'version': '0.18.0',
    'description': 'Toml sorting library',
    'long_description': '# toml-sort\n\n[![pypi-version](https://img.shields.io/pypi/v/toml-sort.svg)](https://python.org/pypi/toml-sort)\n[![license](https://img.shields.io/pypi/l/toml-sort.svg)](https://python.org/pypi/toml-sort)\n[![python-versions](https://img.shields.io/pypi/pyversions/toml-sort.svg)](https://python.org/pypi/toml-sort)\n[![readthedocs-status](https://readthedocs.org/projects/toml-sort/badge/?version=latest)](https://toml-sort.readthedocs.io/en/latest/?badge=latest)\n\nA command line utility to sort and format your toml files. Requires Python 3.6+.\n\nRead the latest documentation here: https://toml-sort.readthedocs.io/en/latest/\n\n## Installation\n\n```bash\n# With pip\npip install toml-sort\n\n# With poetry\npoetry add toml-sort\n```\n\n## Motivation\n\nThis library sorts TOML files, providing the following features:\n\n* Sort tables and Arrays of Tables (AoT)\n* Option to sort non-tables / non-AoT\'s, or not\n* Preserve inline comments\n* Option to preserve top-level document comments, or not\n* Standardize whitespace and indentation\n\nI wrote this library/application because I couldn\'t find any "good" sorting utilities for TOML files. Now, I use this as part of my daily workflow. Hopefully it helps you too!\n\n## Usage\n\nThis project can be used as either a command line utility or a Python library.\n\n### Command line interface\n\n```text\nStdin -> Stdout : cat input.toml | toml-sort\n\nDisk -> Disk    : toml-sort -o output.toml input.toml\n\nLinting         : toml-sort --check input.toml\n\nInplace Disk    : toml-sort --in-place input.toml\n```\n\n## Example\n\nThe following example shows the input, and output, from the CLI with default options.\n\n### Unformatted, unsorted input\n\n```toml\n# My great TOML example\n\n  title = "The example"\n\n[[a-section.hello]]\nports = [ 8001, 8001, 8002 ]\ndob = 1979-05-27T07:32:00Z # First class dates? Why not?\n\n\n\n  [b-section]\n  date = "2018"\n  name = "Richard Stallman"\n\n[[a-section.hello]]\nports = [ 80 ]\ndob = 1920-05-27T07:32:00Z # Another date!\n\n                          [a-section]\n                          date = "2019"\n                          name = "Samuel Roeca"\n```\n\n### Formatted, sorted output\n\n```toml\n# My great TOML example\n\ntitle = "The example"\n\n[a-section]\ndate = "2019"\nname = "Samuel Roeca"\n\n[[a-section.hello]]\nports = [ 8001, 8001, 8002 ]\ndob = 1979-05-27T07:32:00Z # First class dates? Why not?\n\n[[a-section.hello]]\nports = [ 80 ]\ndob = 1920-05-27T07:32:00Z # Another date!\n\n[b-section]\ndate = "2018"\nname = "Richard Stallman"\n```\n\n## Local Development\n\nLocal development for this project is quite simple.\n\n**Dependencies**\n\nInstall the following tools manually.\n\n* [Poetry>=1.0](https://github.com/sdispater/poetry#installation)\n* [GNU Make](https://www.gnu.org/software/make/)\n\n*Recommended*\n\n* [asdf](https://github.com/asdf-vm/asdf)\n\n**Set up development environment**\n\n```bash\nmake setup\n```\n\n**Run Tests**\n\n```bash\nmake test\n```\n\n## Written by\n\nSamuel Roeca, *samuel.roeca@gmail.com*\n',
    'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://toml-sort.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
