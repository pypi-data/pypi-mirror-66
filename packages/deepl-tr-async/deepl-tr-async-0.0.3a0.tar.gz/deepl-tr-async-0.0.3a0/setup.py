# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_tr_async']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.9.0,<0.10.0',
 'environs>=7.3.1,<8.0.0',
 'flake8>=3.7.9,<4.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'linetimer>=0.1.4,<0.2.0',
 'logzero>=1.5.0,<2.0.0',
 'polyglot>=16.7.4,<17.0.0',
 'pycld2>=0.41,<0.42',
 'pyicu>=2.4.3,<3.0.0',
 'pyinstaller>=3.6,<4.0',
 'pyperclip>=1.7.0,<2.0.0',
 'pyppeteer2>=0.2.2,<0.3.0',
 'pyquery>=1.4.1,<2.0.0',
 'pytest-cov>=2.8.1,<3.0.0',
 'python-dotenv>=0.12.0,<0.13.0',
 'tqdm>=4.43.0,<5.0.0']

entry_points = \
{'console_scripts': ['deepl-tr = deepl_tr_async.__main__:main']}

setup_kwargs = {
    'name': 'deepl-tr-async',
    'version': '0.0.3a0',
    'description': 'deepl translate for free, based no pyppeteer',
    'long_description': '# deepl-tr-async ![build](https://github.com/ffreemt/deepl-tr-async/workflows/build/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/deepl-tr-async/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/deepl-tr-async)[![PyPI version](https://badge.fury.io/py/deepl-tr-async.svg)](https://badge.fury.io/py/deepl-tr-async)\ndeepl translate for free with async and proxy support, based on pyppeteer\n\n\n### Pre-installation of libicu\n\n###### For Linux/OSX\n\nE.g.\n* Ubuntu: `sudo apt install libicu-dev`\n* Centos: `yum install libicu`\n* OSX: `brew install icu4c`\n\n###### For Windows\n\nDownload and install the pyicu and pycld2 whl packages for your OS version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2\n\n### Installation\n```pip install deepl-tr-async```\n\nValidate installation\n```\npython -c "import deepl_tr_async; print(deepl_tr_async.__version__)"\n# 0.0.2 or other version info\n```\n\n### Usage\n\n#### from the command line 命令行调用\n* translate the system clipboad (not tested in Linux) 翻译系统剪贴板\n  `deepl-tr`\n* translate text supplied from the command line 翻译终端提供的句子\n  `deepl-tr --copyfrom=false this is a test`\n    <!--img src="img\\sample2.png" height="170px" /-->\n  ![img](https://raw.githubusercontent.com/ffreemt/deepl-tr-async/master/img/copyfrom-false.png)\n* Help 帮助：\n\n  `deepl-tr -?`\n\n  or\n\n  `deepl-tr --helpfull`\n    <!--img src="https://github.com/ffreemt/deepl-tr-async/blob/master/img/copyfrom-false.png" height="170px" /-->\n  ![img](https://raw.githubusercontent.com/ffreemt/deepl-tr-async/master/img/helpfull.png)\n\n#### Programmatic use 程序调用\n```\nimport asyncio\nfrom deepl_tr_async import deepl_tr_async\nfrom deepl_tr_async.google_tr_async import google_tr_async\n\nloop = asyncio.get_event_loop()\n\nsent = \'Global coronavirus pandemic kills more than 30,000\'\n\nres = loop.run_until_complete(deepl_tr_async(sent, to_lang=\'zh\'))\nprint(res)\n# Alternatives:\n# 全球冠状病毒大流行导致超过3万人死亡\n# 全球冠状病毒大流行导致3万多人死亡\n# 全球冠状病毒大流行导致超过30,000人死亡\n# 全球冠状病毒大流行导致3万多人丧生\n\nres = loop.run_until_complete(google_tr_async(sent, to_lang=\'zh\'))\nprint(res)\n# 全球冠状病毒大流行杀死超过30,000人\n\ntasks = [deepl_tr_async(sent, to_lang=\'zh\'), google_tr_async(sent, to_lang=\'zh\')]\n_ = asyncio.gather(*tasks)\nres = loop.run_until_complete(_)\nprint(res)\n[\'Alternatives:\\n全球冠状病毒大流行导致超过3万人死亡\\n全球冠状病毒大流行导致3万多人死亡\\n全球冠状病毒大流行导致超过30,000人死亡\\n全球冠状病毒大流行导致3万多人丧生\', \'全球冠状病毒大流行杀死超过30,000人\']\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/deepl-tr-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
