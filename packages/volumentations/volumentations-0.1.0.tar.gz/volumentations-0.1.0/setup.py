# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volumentations', 'volumentations.augmentations', 'volumentations.core']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.6.0,<2.0.0',
 'numpy>=1.18.3,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'volumentations',
    'version': '0.1.0',
    'description': 'Point augmentations library as hard-fork of albu-team/albumentations',
    'long_description': '[![Tests](https://github.com/kumuji/volumentations/workflows/Tests/badge.svg)](https://github.com/kumuji/volumentations/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/kumuji/volumentations/branch/master/graph/badge.svg)](https://codecov.io/gh/kumuji/volumentations)\n\n',
    'author': 'kumuji',
    'author_email': 'alexey@nekrasov.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kumuji/volumentations',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
