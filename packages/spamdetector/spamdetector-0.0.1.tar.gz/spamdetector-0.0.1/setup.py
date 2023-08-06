# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spamdetector']

package_data = \
{'': ['*'], 'spamdetector': ['models/*']}

install_requires = \
['joblib>=0.14.1,<0.15.0', 'scikit-learn>=0.22.2,<0.23.0']

setup_kwargs = {
    'name': 'spamdetector',
    'version': '0.0.1',
    'description': 'Spam Classifier/Detector ML Package',
    'long_description': None,
    'author': 'Rohit Kumar',
    'author_email': 'rohit1998kg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
