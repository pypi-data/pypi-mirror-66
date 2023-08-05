# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.osc']

package_data = \
{'': ['*']}

install_requires = \
['dirty-cat>=0.0.5,<0.0.6',
 'joblib>=0.14.0,<0.15.0',
 'pandas>=1.0.3,<2.0.0',
 'scikit-learn==0.20.3',
 'tensorflow-estimator==2.1.0',
 'tensorflow==2.1.0']

setup_kwargs = {
    'name': 'cognite-open-set-classifier',
    'version': '0.2.0',
    'description': 'Open-set classifier',
    'long_description': None,
    'author': 'Rebecca Wiborg Seyfarth',
    'author_email': 'rebecca.wiborg.seyfarth@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
