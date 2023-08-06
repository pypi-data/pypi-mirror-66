# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfpy', 'tfpy.core']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0', 'terraformpy==1.2.3', 'typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['tfpy = tfpy.main:app']}

setup_kwargs = {
    'name': 'tfpy',
    'version': '0.1.0',
    'description': 'Create Terraform resources using Python',
    'long_description': None,
    'author': 'Rémy Greinhofer',
    'author_email': 'remy.greinhofer@gmail.com',
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
