# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logupdate']

package_data = \
{'': ['*']}

install_requires = \
['ansiwrap>=0.8.4,<0.9.0', 'cursor>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'logupdate',
    'version': '0.3.1',
    'description': 'Log by overwriting the previous output in the terminal',
    'long_description': '# logupdate.py\n\n[![PyPI](https://img.shields.io/pypi/v/logupdate.svg)](https://pypi.org/project/logupdate/)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/logupdate.svg)](https://pypi.python.org/pypi/logupdate)\n[![Build Status](https://travis-ci.org/AdrieanKhisbe/logupdate.py.svg?branch=master)](https://travis-ci.org/AdrieanKhisbe/logupdate.py)\n\n> Log by overwriting the previous output in the terminal. \n> Useful for rendering progress bars, animations, etc.\n> (Port of [sindresorhus/log-update](https://github.com/sindresorhus/log-update) from js to python)\n\n## Install\nJust pip install it, and you\'re good to go.\n\n```bash\npip install logupdate\n```\n\n## Usage\n```python\nfrom logupdate import logupdate\nfrom time import sleep\n\nlogupdate("Hello, a secret is about to be said to you")\nsleep(1)\nlogupdate("You can pimp your interactive commands with logupdate")\nsleep(1)\nlogupdate("Don\'t forget the secret ;)")\nsleep(1)\nlogupdate.clear().done()\n```\n\n## Examples\n\nYou can find some example in the dedicated [examples](./examples) folder.\n\n## API\n- `logupdate(text, ...)`: log to stdout (overwriting previous input)\n- `logupdate.clear([restore_cursor=None])`: Clear previous logged output. This can also restore the cursor if asked.\n- `logupdate.done([restore_cursor=None])`: Persist the logged output. This enable to start a new "log session" below.\n  This restores the cursor unless you ask not to.\n\n- `logupdate.stderr(text, ...)`: log to stderr\n- `logupdate.stderr.clear([restore_cursor=None])`: clear stderr.\n- `logupdate.stderr.done([restore_cursor=None])`:  persist stderr.\n\n- `logupdate.create(stream, [show_cursor=False])` : return a `logupdate` method dedicated to log to given `stream`.\n\n## License\nMIT © [AdrieanKhisbe](https://github.com/AdrieanKhisbe)\n',
    'author': 'Adriean Khisbe',
    'author_email': 'adriean.khisbe@live.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CoorpAcademy/pino.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
