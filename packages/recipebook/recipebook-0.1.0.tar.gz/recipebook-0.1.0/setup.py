# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recipebook']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'recipebook',
    'version': '0.1.0',
    'description': "I'm writing a cookbook to learn Python, Postgresql, and other potential tools.",
    'long_description': None,
    'author': 'Mike Martino',
    'author_email': 'mikemartino86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
