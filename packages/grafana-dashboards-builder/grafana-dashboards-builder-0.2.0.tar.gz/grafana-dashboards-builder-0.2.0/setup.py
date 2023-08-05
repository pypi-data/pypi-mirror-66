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
    'version': '0.2.0',
    'description': 'A wrapper around grafanalib which simplifies generating multiple dashboards.',
    'long_description': "# Grafana Dashboards Builder\n\nA wrapper around [grafanalib](https://github.com/weaveworks/grafanalib) which simplifies generating multiple dashboards.\n\n## Why?\n\nGrafanalib is a fantastic tool which lets you generate Grafana dashboards from simple Python scripts. Unfortunately, it can only read single files as dashboard sources and doesn't have a concept of multiple output directories. Those limitations make it hard to provision an entire Grafana instance with many folders and multiple dashboard sources.\n\nGrafana Dashboard Builder recursively finds all `.dashboard.py` files in a directory tree. It generates dashboards and places them in a subdirectories which represent [Grafana folders](https://grafana.com/docs/grafana/latest/reference/dashboard_folders/).\n\nIt's written with Kubernetes in mind so it can also generate nested output directory structure even when loading sources mounted from a flat ConfigMap (see [examples](#sources-in-a-configmap) below).\n\n\n## Installation\n\n    pip install grafana-dashboards-builder\n\n\n## Usage\n\n    grafana-dashboards-builder [OPTIONS] INPUT_DIR [OUTPUT_DIR]\n\n    INPUT_DIR is the directory tree with dashboard sources.\n\n    OUTPUT_DIR is the directory where generated dashboards are placed (defaults to ./out).\n\n    Options:\n    --from-configmap  generate output directories based on a source files prefix and a '--' separator\n    --help            Show this message and exit.\n\n\n## Examples\n\n### Sources in nested directories\n\nGrafana supports only one level of depth for [folders](https://grafana.com/docs/grafana/latest/reference/dashboard_folders/). So even when dashboard sources are nested in multiple subdirectories the output dashboards will have only one parent directory (the most shallow one). Source dashboards that don't have any parent directory will be placed in the default `General` folder.\n\nFor example, given a following input directory tree:\n\n    dashboards_in/\n        main.dashboard.py\n        kubernetes/\n            workloads/\n                pods.dashboard.py\n                jobs.dashboard.py\n            nodes/\n                nodes.dashboard.py\n        nginx/\n            nginx_health.dashboard.py\n\nA following output directory will be generated:\n\n    dashboards_out/\n        General/\n            main.json\n        Kubernetes/\n            pods.json\n            jobs.json\n            nodes.json\n        Nginx/\n            nginx_health.json\n\n### Sources in a ConfigMap\n\nWhen running Grafana in Kubernetes cluster it's possible to run Grafana Dashboard Builder as a sidecar which loads dashboard sources from a ConfigMap and generates them into Grafana's `/var/lib/grafana/dashboards` directory.\n\nConfigMaps don't support nested directory structures so to enable mapping dashboards to different folders we can prefix the sources filenames with a `folder--` prefix. When Grafana Dashboard Builder runs with `--from-configmap` flag, it parses the filenames and generates output directories based on found prefixes. Filenames without a prefix will be placed in the default `General` folder.\n\nFor example, given a following input directory:\n\n    dashboards_in/\n        main.dashboard.py\n        kubernetes--pods.dashboard.py\n        kubernetes--jobs.dashboard.py\n        nginx--nginx_health.dashboard.py\n        \nA following output directory will be generated:\n\n    dashboards_out/\n        General/\n            main.json\n        Kubernetes/\n            pods.json\n            jobs.json\n        Nginx/\n            nginx_health.json\n",
    'author': 'Grzegorz Dlugoszewski',
    'author_email': 'pypi@grdl.dev',
    'maintainer': 'Grzegorz Dlugoszewski',
    'maintainer_email': 'pypi@grdl.dev',
    'url': 'https://gitlab.com/grdl/grafana-dashboards-builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
