# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recipebook']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['example = recipebook.example:main']}

setup_kwargs = {
    'name': 'recipebook',
    'version': '0.1.1',
    'description': "I'm writing a cookbook to learn Python, Postgresql, and other potential tools.",
    'long_description': "recipebook\n==========\n\nI'm writing a cookbook to learn Python, Postgresql, and other potential tools.\n\n# Prerequisites\n\nInstall `poetry` for managing virtual environment (similar to `venv` or `pipenv`):\n\n    ```\n    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3\n    ```\n\nRead more about `poetry`: https://python-poetry.org/\n\n_Optional_: I've installed `pyenv` to manage versions of Python on my system. Read more about `pyenv`: https://github.com/pyenv/pyenv\n\n# Build\n\n```\npoetry install\npoetry run example\n```\n\n# Package\n\n```\npoetry build\n```\n\n# Deploy\n\n```\npoetry publish\n```",
    'author': 'Mike Martino',
    'author_email': 'mikemartino86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mikemartino/recipebook',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
