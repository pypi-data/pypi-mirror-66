# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cv_py', 'cv_py.data', 'cv_py.embed', 'cv_py.viz']

package_data = \
{'': ['*']}

install_requires = \
['dask[complete]>=2.13.0,<3.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyarrow>=0.16.0,<0.17.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'tqdm>=4.43.0,<5.0.0']

extras_require = \
{'flair': ['flair>=0.4.5,<0.5.0']}

entry_points = \
{'console_scripts': ['cv-download = cv.data.resource:download']}

setup_kwargs = {
    'name': 'cv-py',
    'version': '0.1.1',
    'description': 'Collection of tools and techniques to kick-start analysis of the COVID-19 Research Challenge Dataset ',
    'long_description': None,
    'author': 'Thurston Sexton',
    'author_email': 'thurston.sexton@nist.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
