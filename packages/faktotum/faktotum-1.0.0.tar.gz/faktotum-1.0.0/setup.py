# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faktotum',
 'faktotum.research',
 'faktotum.research.clustering',
 'faktotum.research.corpus',
 'faktotum.research.exploration',
 'faktotum.research.knowledge',
 'faktotum.research.linking',
 'faktotum.research.modeling',
 'faktotum.research.ontologia',
 'faktotum.research.vendor']

package_data = \
{'': ['*'], 'faktotum.research.vendor': ['droc/*', 'smartdata/*']}

install_requires = \
['numpy>=1.16.1,<2.0.0',
 'pandas>=0.25.3,<0.26.0',
 'strsimpy>=0.1.3,<0.2.0',
 'syntok>=1.2.2,<2.0.0',
 'torch>=1.4.0,<2.0.0',
 'tqdm>=4.41.1,<5.0.0',
 'transformers>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'faktotum',
    'version': '1.0.0',
    'description': 'Extracting information from unstructured text.',
    'long_description': None,
    'author': 'Severin Simmler',
    'author_email': 'severin.simmler@stud-mail.uni-wuerzburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
