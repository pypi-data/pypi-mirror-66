# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cv', 'cv.data', 'cv.embed', 'cv.viz']

package_data = \
{'': ['*']}

install_requires = \
['dask[complete]>=2.13.0,<3.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyarrow>=0.16.0,<0.17.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'scispacy>=0.2.4,<0.3.0',
 'textacy>=0.10.0,<0.11.0',
 'tqdm>=4.43.0,<5.0.0']

entry_points = \
{'console_scripts': ['cv-download = cv.data.cdcs:download']}

setup_kwargs = {
    'name': 'cv-py',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'tbsexton',
    'author_email': 'tbsexton@asu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
