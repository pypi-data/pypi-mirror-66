# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getostheme']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['getostheme = getostheme:cli']}

setup_kwargs = {
    'name': 'getostheme',
    'version': '2020.3',
    'description': 'Use this module to get the OS theme (dark/light)',
    'long_description': '[![Github top language](https://img.shields.io/github/languages/top/FHPythonUtils/GetOSTheme.svg?style=for-the-badge)](../../)\n[![Codacy grade](https://img.shields.io/codacy/grade/9f0a36e773394f15844ab296597e9732.svg?style=for-the-badge)](https://www.codacy.com/manual/FHPythonUtils/GetOSTheme)\n[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/GetOSTheme.svg?style=for-the-badge)](../../)\n[![Issues](https://img.shields.io/github/issues/FHPythonUtils/GetOSTheme.svg?style=for-the-badge)](../../issues)\n[![License](https://img.shields.io/github/license/FHPythonUtils/GetOSTheme.svg?style=for-the-badge)](/LICENSE.md)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/GetOSTheme.svg?style=for-the-badge)](../../commits/master)\n[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/GetOSTheme.svg?style=for-the-badge)](../../commits/master)\n[![PyPI](https://img.shields.io/pypi/dm/getostheme.svg?style=for-the-badge)](https://pypi.org/project/getostheme/)\n\n# GetOSTheme\n\n<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">\n\n## Use\n\n### From import\n\nUse one of the following functions in your program\n\n```python\ndef isLightMode():\n\t"""Call isLightMode_OS\n\n\tReturns:\n\t\tbool: OS is in light mode\n\t"""\n\ndef isDarkMode():\n\t"""\n\tReturns:\n\t\tbool: OS is in dark mode\n\t"""\n```\n\n### From CLI\nCall from the command line\n\n```bash\ngetostheme\n```\n\n## Install With PIP\n\n```python\npip install getostheme\n```\n\nHead to https://pypi.org/project/getostheme/ for more info\n\n## Language information\n### Built for\nThis program has been written for Python 3 and has been tested with\nPython version 3.8.0 <https://www.python.org/downloads/release/python-380/>.\n\n## Install Python on Windows\n### Chocolatey\n```powershell\nchoco install python\n```\n### Download\nTo install Python, go to <https://www.python.org/> and download the latest\nversion.\n\n## Install Python on Linux\n### Apt\n```bash\nsudo apt install python3.8\n```\n\n## How to run\n### With VSCode\n1. Open the .py file in vscode\n2. Ensure a python 3.8 interpreter is selected (Ctrl+Shift+P > Python:Select Interpreter > Python 3.8)\n3. Run by pressing Ctrl+F5 (if you are prompted to install any modules, accept)\n### From the Terminal\n```bash\n./[file].py\n```\n\n\n## Changelog\nSee the [CHANGELOG](/CHANGELOG.md) for more information.\n\n\n## Download\n### Clone\n#### Using The Command Line\n1. Press the Clone or download button in the top right\n2. Copy the URL (link)\n3. Open the command line and change directory to where you wish to\nclone to\n4. Type \'git clone\' followed by URL in step 2\n```bash\n$ git clone https://github.com/FHPythonUtils/GetOSTheme\n```\n\nMore information can be found at\n<https://help.github.com/en/articles/cloning-a-repository>\n\n#### Using GitHub Desktop\n1. Press the Clone or download button in the top right\n2. Click open in desktop\n3. Choose the path for where you want and click Clone\n\nMore information can be found at\n<https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop>\n\n### Download Zip File\n\n1. Download this GitHub repository\n2. Extract the zip archive\n3. Copy/ move to the desired location\n\n\n## Licence\nMixed Licenses\n(See the [LICENSE](/LICENSE.md) for more information.)\n',
    'author': 'FredHappyface',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FredHappyface/Python.GetOSTheme',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
