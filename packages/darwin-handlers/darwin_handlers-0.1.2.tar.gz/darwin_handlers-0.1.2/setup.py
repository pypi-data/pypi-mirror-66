# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['darwin_handlers',
 'darwin_handlers.config',
 'darwin_handlers.config.backtest',
 'darwin_handlers.config.general',
 'darwin_handlers.config.reinforcement',
 'darwin_handlers.core',
 'darwin_handlers.data',
 'darwin_handlers.environments',
 'darwin_handlers.handlers',
 'darwin_handlers.handlers.abstracts',
 'darwin_handlers.handlers.files',
 'darwin_handlers.handlers.files.models',
 'darwin_handlers.handlers.ordering',
 'darwin_handlers.handlers.strategy',
 'darwin_handlers.search',
 'darwin_handlers.search.backtesting',
 'darwin_handlers.search.backtesting.accessors',
 'darwin_handlers.search.backtesting.topics',
 'darwin_handlers.search.ordering',
 'darwin_handlers.stochastic',
 'darwin_handlers.stochastic.generators',
 'darwin_handlers.stochastic.utils',
 'darwin_handlers.utils',
 'darwin_handlers.utils.properties',
 'darwin_handlers.utils.slippage',
 'darwin_handlers.utils.trades']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2.14.0,<3.0.0',
 'faker>=4.0.3,<5.0.0',
 'jamboree==0.7.2',
 'matplotlib>=3.2.1,<4.0.0',
 'maya>=0.6.1,<0.7.0',
 'pandas_datareader>=0.8.1,<0.9.0',
 'skorch>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'darwin-handlers',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Kevin Hill',
    'author_email': 'kivo360@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0',
}


setup(**setup_kwargs)
