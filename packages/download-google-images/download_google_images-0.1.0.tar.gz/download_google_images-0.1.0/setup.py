# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['download_google_images']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=7.1.1,<8.0.0',
 'requests>=2.23.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'typer[all]>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['download-google-images = '
                     'download_google_images.main:app']}

setup_kwargs = {
    'name': 'download-google-images',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Adarsh1999',
    'author_email': 'adarshguptamaurya@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
