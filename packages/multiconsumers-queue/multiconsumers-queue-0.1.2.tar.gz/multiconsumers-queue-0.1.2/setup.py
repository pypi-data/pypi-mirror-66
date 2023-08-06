# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multiconsumers_queue']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.5,<0.16.0', 'attrs>=19.3.0,<20.0.0', 'loguru>=0.4.1,<0.5.0']

extras_require = \
{'click': ['click>=7.1.1,<8.0.0']}

setup_kwargs = {
    'name': 'multiconsumers-queue',
    'version': '0.1.2',
    'description': 'Wrapper for queue based producer/consumers parallel tasks execution',
    'long_description': '<p>\n<a href="https://www.python.org/downloads/release/python-370"><img alt="Python 3.7" src="https://img.shields.io/badge/python-3.7-blue.svg"></a>\n<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n# multiconsumers-queue-cli\nWrapper for queue based producer/consumers parallel tasks execution\n\n#### Futures:\n- graceful shutdown by ^C\n- producer/consumer errors handling out of the box\n- scheduled tasks statistics logging \n\n#### Examples:\n- [with ThreadPoolExecutor](examples/cli-threads.py) for I/O bound tasks\n    ```\n    Usage: cli-threads.py [OPTIONS]\n    \n      Demo script with ThreadPoolExecutor\n    \n    Options:\n      --workers INTEGER     How many workers will be started  [default: 5]\n      --limit INTEGER       How many items can be produced  [default: 50]\n      --logging-level TEXT  Logging level  [default: INFO]\n      --help                Show this message and exit.\n    ```\n\n#### References:\n- [Concurrency with Python: Threads and Locks](https://bytes.yingw787.com/posts/2019/01/12/concurrency_with_python_threads_and_locks/)\n- [The tragic tale of the deadlocking Python queue](https://codewithoutrules.com/2017/08/16/concurrency-python/)\n- [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/#setting-up-a-python-project-using-poetry)\n',
    'author': 'IaroslavR',
    'author_email': 'iarruss@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/IaroslavR/multiconsumers-queue',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
