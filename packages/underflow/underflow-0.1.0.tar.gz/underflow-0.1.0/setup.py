# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['underflow']

package_data = \
{'': ['*']}

install_requires = \
['chalice>=1.13.1,<2.0.0',
 'click-spinner>=0.1.8,<0.2.0',
 'dacite>=1.4.0,<2.0.0',
 'fastapi>=0.54.1,<0.55.0',
 'httpx>=0.12.1,<0.13.0',
 'pydantic[dotenv]>=1.4,<2.0',
 'python-telegram-bot>=12.6.1,<13.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'typer>=0.1.1,<0.2.0',
 'uvicorn>=0.11.3,<0.12.0']

entry_points = \
{'console_scripts': ['underflow = underflow.cli:app']}

setup_kwargs = {
    'name': 'underflow',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Santos',
    'author_email': 'daniel.martins@lumedigital.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
