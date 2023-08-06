# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_legion', 'fast_legion.schemas']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.54.1,<0.55.0', 'pydantic>=1.5,<2.0', 'pyjwt>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'fast-legion',
    'version': '0.1.0',
    'description': "A JWT Security Bundle that let's you choose your favorite data layer for the FastAPI framework.",
    'long_description': None,
    'author': 'David Emmanuel Asaf',
    'author_email': 'me@davideasaf.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
