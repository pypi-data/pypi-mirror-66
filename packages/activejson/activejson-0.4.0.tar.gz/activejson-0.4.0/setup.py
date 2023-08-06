# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['activejson']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'activejson',
    'version': '0.4.0',
    'description': 'A convenient library to deal with large json data',
    'long_description': "# Activejson\n\n[![PyPI version](https://badge.fury.io/py/activejson.svg)](https://badge.fury.io/py/activejson)\n[![Tests](https://github.com/BentoBox-Project/activejson/workflows/Tests/badge.svg)](https://github.com/BentoBox-Project/activejson/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/BentoBox-Project/activejson/branch/master/graph/badge.svg)](https://codecov.io/gh/BentoBox-Project/activejson)\n\n> A convenient library to deal with large json data\n\nA convenient library to deal with large json data. The purpose of this package is help to deal with complex json-like data, converting them into a more manageable data structure.\n\n## Installation\n\nOS X & Linux:\n\nFrom PYPI\n\n```sh\n$ pip3 install activejson\n```\n\nfrom the source\n\n```sh\n$ git clone https://github.com/dany2691/activejson.git\n$ cd activejson\n$ python3 setup.py install\n```\n\n## Usage example\n\nYou can flat a complex dict the next way:\n\n```python\ncomplex_json = {\n    'cat': {'grass': 'feline', 'mud': 'you never know', 'horse': 'my joke'},\n    'dolphin': [\n        {'tiger': [{'bird': 'blue jay'}, {'fish': 'dolphin'}]},\n        {'cat2': 'feline'},\n       {'dog2': 'canine'}\n  ],\n  'dog': 'canine'\n}\n```\n\n```python\nfrom activejson import flatten_json\n\nflatten_complex_json = flatten_json(complex_json)\n\nprint(flatten_complex_json)\n```\n\nThe result could be the next:\n\n```sh\n{\n    'cat_grass': 'feline',\n    'cat_horse': 'my joke',\n    'cat_mud': 'you never know',\n    'dog': 'canine',\n    'dolphin_0_tiger_0_bird': 'blue jay',\n    'dolphin_0_tiger_1_fish': 'dolphin',\n    'dolphin_1_cat2': 'feline',\n    'dolphin_2_dog2': 'canine'\n}\n```\n\nOn the other hand, is possible to convert that dict into an object with dynamic attributes:\n\n```python\nfrom activejson import FrozenJSON\n\nfrozen_complex_json = FrozenJSON(complex_json)\n\nprint(frozen_complex_json.cat.grass)\nprint(frozen_complex_json.cat.mud)\nprint(frozen_b.dolphin[2].dog2)\n```\n\nThe result could be the next:\n\n```sh\n'feline'\n'you never know'\n'canine'\n```\n\nTo retrieve the underlying json, is possible to use the json property:\n\n```python\nfrozen_complex_json.json\n```\n\n```sh\n{\n    'cat_grass': 'feline',\n    'cat_horse': 'my joke',\n    'cat_mud': 'you never know',\n    'dog': 'canine',\n    'dolphin_0_tiger_0_bird': 'blue jay',\n    'dolphin_0_tiger_1_fish': 'dolphin',\n    'dolphin_1_cat2': 'feline',\n    'dolphin_2_dog2': 'canine'\n}\n```\n\n# Development setup\n\nThis project uses __Poetry__ for dependecy resolution. It's a kind of mix between\npip and virtualenv. Follow the next instructions to setup the development enviroment.\n\n\n```sh\n$ pip install poetry\n```\n\n\n```sh\n$ git clone https://github.com/dany2691/activejson.git\n$ cd activejson\n$ poetry install\n```\n\nTo run the test-suite, inside the pybundler directory:\n\n```shell\n$ poetry run pytest test/ -vv\n```\n\n## Meta\n\nDaniel Omar Vergara Pérez – [@__danvergara __](https://twitter.com/__danvergara__) – daniel.omar.vergara@gmail.com -- [github.com/danvergara](https://github.com/danvergara)\n\nValery Briz - [@valerybriz](https://twitter.com/valerybriz) -- [github.com/valerybriz](https://github.com/valerybriz)\n\n\n\n## Contributing\n\n1. Fork it (<https://github.com/BentoBox-Project/activejson>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am 'Add some fooBar'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n",
    'author': 'Daniel Omar Vergara Pérez',
    'author_email': 'daniel.omar.vergara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
