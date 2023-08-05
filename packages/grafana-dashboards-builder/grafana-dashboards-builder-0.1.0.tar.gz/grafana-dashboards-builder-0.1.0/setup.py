# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['builder']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'grafanalib>=0.5.5,<0.6.0']

entry_points = \
{'console_scripts': ['grafana-dashboards-builder = builder.builder:build']}

setup_kwargs = {
    'name': 'grafana-dashboards-builder',
    'version': '0.1.0',
    'description': 'A wrapper around grafanalib which simplifies generating multiple dashboards.',
    'long_description': None,
    'author': 'Grzegorz Dlugoszewski',
    'author_email': 'pypi@grdl.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
