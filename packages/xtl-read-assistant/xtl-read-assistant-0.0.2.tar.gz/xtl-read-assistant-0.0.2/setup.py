# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xtl_read_assistant']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.9.0,<0.10.0',
 'deepl-tr-async>=0.0.2,<0.0.3',
 'environs>=7.3.1,<8.0.0',
 'janus>=0.4.0,<0.5.0',
 'logzero>=1.5.0,<2.0.0',
 'polyglot>=16.7.4,<17.0.0',
 'pynput>=1.6.8,<2.0.0',
 'pyperclip>=1.7.0,<2.0.0',
 'python-dotenv>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['read-assist = xtl_read_assistant.read_assist:main']}

setup_kwargs = {
    'name': 'xtl-read-assistant',
    'version': '0.0.2',
    'description': 'X as a third language reading assistant',
    'long_description': '# xtl-read-assistant ![build](https://github.com/ffreemt/xtl-read-assistant/workflows/build/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/xtl-read-assistant/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/xtl-read-assistant)[![PyPI version](https://badge.fury.io/py/xtl-read-assistant.svg)](https://badge.fury.io/py/xtl-read-assistant)\nx as a third language reading assistant tool\n\n### Pre-installation of libicu\n\n###### For Linux/OSX\n\nE.g.\n* Ubuntu: `sudo apt install libicu-dev`\n* Centos: `yum install libicu`\n* OSX: `brew install icu4c`\n\n###### For Windows\n\nDownload and install the pyicu and pycld2 whl packages for your OS version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2\n\n### Installation\n```pip install xtl-read-assistant```\n\nValidate installation\n```\npython -c "import xtl_read_assistant; print(xtl_read_assistant.__version__)"\n# 0.0.2 or other version info\n```\n#### Patch `pyppeteer/connection.py`\n\nThe pyppeteer package does not work too well with websockets 7+. Either downgrade the websockets to 6 or manually perform the following patch.\n\nChange site-packages\\pyppeteer\\connection.py  `line 44`  to:\n`\n            # self._url, max_size=None, loop=self._loop)\n            self._url, max_size=None, loop=self._loop, ping_interval=None, ping_timeout=None)\n`\n\n### Usage\n\nRun `read-assist.exe`; Copy text to the clipboard (`ctrl-c`); Activate hotkey (`ctrl-alt-g`)\n\nThe translated text is stored in the clipboard.\n\n#### default setup: --mother-lang=zh --second-lang=en --third-lang=de\n`read-assist`\n\n`ctrl-alt-g`: to activate clipboard translation\n`ctrl-alt-x`: to exit\n\n#### other setup exmaple: --mother-lang=zh --second-lang=en --third-lang=fr\n\n`read-assist --third-lang=fr`\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/xtl-read-assistant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
