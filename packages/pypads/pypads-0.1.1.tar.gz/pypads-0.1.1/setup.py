# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypads',
 'pypads.autolog',
 'pypads.autolog.wrapping',
 'pypads.bindings',
 'pypads.bindings.resources',
 'pypads.bindings.resources.mapping',
 'pypads.functions',
 'pypads.functions.analysis',
 'pypads.functions.analysis.validation',
 'pypads.functions.analysis.validation.visitors',
 'pypads.functions.loggers',
 'pypads.functions.loggers.mlflow',
 'pypads.functions.post_run',
 'pypads.functions.pre_run',
 'pypads.parallel']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=19.3.0,<20.0.0',
 'cloudpickle>=1.3.0,<2.0.0',
 'loguru>=0.4.1,<0.5.0',
 'mlflow>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'pypads',
    'version': '0.1.1',
    'description': 'PyPaDS aims to to add tracking functionality to machine learning libraries.',
    'long_description': None,
    'author': 'Thomas Weißgerber',
    'author_email': 'thomas.weissgerber@uni-passau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
