# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catpandoc']

package_data = \
{'': ['*']}

install_requires = \
['art>=4.6,<5.0',
 'catimage>=2020.5,<2021.0',
 'cli2gui>=2020.7,<2021.0',
 'emoji>=0.5.4,<0.6.0',
 'pygments>=2.6.1,<3.0.0',
 'pypandoc>=1.5,<2.0']

entry_points = \
{'console_scripts': ['catpandoc = catpandoc.application:cli']}

setup_kwargs = {
    'name': 'catpandoc',
    'version': '2020.2',
    'description': 'Cat multiple document files to the terminal',
    'long_description': '[![Github top language](https://img.shields.io/github/languages/top/FHPythonUtils/CatPandoc.svg?style=for-the-badge)](../../)\n[![Codacy grade](https://img.shields.io/codacy/grade/[codacy-proj-id].svg?style=for-the-badge)](https://www.codacy.com/manual/FHPythonUtils/CatPandoc)\n[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/CatPandoc.svg?style=for-the-badge)](../../)\n[![Issues](https://img.shields.io/github/issues/FHPythonUtils/CatPandoc.svg?style=for-the-badge)](../../issues)\n[![License](https://img.shields.io/github/license/FHPythonUtils/CatPandoc.svg?style=for-the-badge)](/LICENSE.md)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/CatPandoc.svg?style=for-the-badge)](../../commits/master)\n[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/CatPandoc.svg?style=for-the-badge)](../../commits/master)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/catpandoc.svg?style=for-the-badge)](https://pypi.org/project/catpandoc/)\n[![PyPI Version](https://img.shields.io/pypi/v/catpandoc.svg?style=for-the-badge)](https://pypi.org/project/catpandoc/)\n\n<!-- omit in toc -->\n# CatPandoc\n\n<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">\n\nCat multiple documents to the terminal. The continuation of CatMD\n\n- [Features](#features)\n\t- [Document Compatability](#document-compatability)\n\t- [Terminal \'rendering\'](#terminal-rendering)\n- [Roadmap](#roadmap)\n- [Install With PIP](#install-with-pip)\n- [Use](#use)\n\t- [CLI](#cli)\n\t- [Import](#import)\n- [Language information](#language-information)\n\t- [Built for](#built-for)\n- [Install Python on Windows](#install-python-on-windows)\n\t- [Chocolatey](#chocolatey)\n\t- [Download](#download)\n- [Install Python on Linux](#install-python-on-linux)\n\t- [Apt](#apt)\n- [How to run](#how-to-run)\n\t- [With VSCode](#with-vscode)\n\t- [From the Terminal](#from-the-terminal)\n- [Changelog](#changelog)\n- [Download](#download-1)\n\t- [Clone](#clone)\n\t\t- [Using The Command Line](#using-the-command-line)\n\t\t- [Using GitHub Desktop](#using-github-desktop)\n\t- [Download Zip File](#download-zip-file)\n- [Licence](#licence)\n- [Screenshots](#screenshots)\n\t- [Desktop](#desktop)\n\t- [Themes](#themes)\n\n## Features\n\n### Document Compatability\nLightweight markup formats\n- Markdown (including CommonMark and GitHub-flavored Markdown)\n- reStructuredText\n- Emacs Org-Mode\n- Emacs Muse\n- Textile\n- txt2tags\n\nHTML formats\n- (X)HTML 4\n- HTML5\n\nEbooks\n- EPUB version 2 or 3\n- FictionBook2\n\nDocumentation formats\n- Haddock markup\n\nRoff formats\n- roff man\n\nTeX formats\n- LaTeX\n\nXML formats\n- DocBook version 4 or 5\n- JATS\n\nOutline formats\n- OPML\n\nData formats\n- CSV tables\n\nWord processor formats\n- Microsoft Word docx\n- OpenOffice/LibreOffice ODT\n\nInteractive notebook formats\n- Jupyter notebook (ipynb)\n\n\nWiki markup formats\n- MediaWiki markup\n- DokuWiki markup\n- TikiWiki markup\n- TWiki markup\n- Jira wiki markup\n\n### Terminal \'rendering\'\nHighlights the following:\n- Headers 1-6\n- Unordered and ordered lists\n- Block quotes\n- Bold, Italic, Strikethrough, inline code\n- Line Break (br)\n\nRenders the following\n- Tables\n- Images (uses catimage for this so they can look a bit blurry...)\n\nHiglights code blocks\n- Uses pygments for code syntax highlighting\n\n## Roadmap\nFor completed components, see the changelog (link below)\n\n|Feature|Description|Status|\n|---|---|---|\n|pandoc2pysimplegui.py|Generate PySimpleGUI widgets|-|\n\n## Install With PIP\n\n```python\npip install catpandoc\n```\n\nHead to https://pypi.org/project/catpandoc/ for more info\n\n\n## Use\n\n### CLI\n```bash\nusage: application.py [-h] [--width WIDTH] [--theme THEME] file\n```\n\n### Import\nTake a look at test/catcomplex.py for an example of how to use catpandoc in your own\nproject. Or take a look at the example below\n```python\nimport json\nimport pypandoc\nfrom catpandoc import pandoc2ansi, processpandoc\n\noutput = json.loads(pypandoc.convert_file("cheatsheet.md", \'json\'))\nfor block in output["blocks"]:\n\tpandoc = pandoc2ansi.Pandoc2Ansi(130, 5, (4, 0, 0))\n\tprocesspandoc.processBlock(block, pandoc)\n\tprint(pandoc.genOutput())\n```\n\n\n## Language information\n### Built for\nThis program has been written for Python 3 and has been tested with\nPython version 3.8.0 <https://www.python.org/downloads/release/python-380/>.\n\n## Install Python on Windows\n### Chocolatey\n```powershell\nchoco install python\n```\n### Download\nTo install Python, go to <https://www.python.org/> and download the latest\nversion.\n\n## Install Python on Linux\n### Apt\n```bash\nsudo apt install python3.8\n```\n\n## How to run\n### With VSCode\n1. Open the .py file in vscode\n2. Ensure a python 3.8 interpreter is selected (Ctrl+Shift+P > Python:Select\nInterpreter > Python 3.8)\n3. Run by pressing Ctrl+F5 (if you are prompted to install any modules, accept)\n### From the Terminal\n```bash\n./[file].py\n```\n\n\n## Changelog\nSee the [CHANGELOG](/CHANGELOG.md) for more information.\n\n\n## Download\n### Clone\n#### Using The Command Line\n1. Press the Clone or download button in the top right\n2. Copy the URL (link)\n3. Open the command line and change directory to where you wish to\nclone to\n4. Type \'git clone\' followed by URL in step 2\n```bash\n$ git clone https://github.com/FHPythonUtils/CatPandoc\n```\n\nMore information can be found at\n<https://help.github.com/en/articles/cloning-a-repository>\n\n#### Using GitHub Desktop\n1. Press the Clone or download button in the top right\n2. Click open in desktop\n3. Choose the path for where you want and click Clone\n\nMore information can be found at\n<https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop>\n\n### Download Zip File\n\n1. Download this GitHub repository\n2. Extract the zip archive\n3. Copy/ move to the desired location\n\n\n## Licence\nMIT License\nCopyright (c) FredHappyface\n(See the [LICENSE](/LICENSE.md) for more information.)\n\n\n## Screenshots\n\n### Desktop\n<div>\n<img src="readme-assets/screenshots/desktop/screenshot-0.png" alt="Screenshot 1" width="600">\n<img src="readme-assets/screenshots/desktop/screenshot-1.png" alt="Screenshot 2" width="600">\n<img src="readme-assets/screenshots/desktop/screenshot-2.png" alt="Screenshot 3" width="600">\n</div>\n\n### Themes\n\n<div>\n<img src="readme-assets/screenshots/themes/theme-1.png" alt="Screenshot 1" width="200">\n<img src="readme-assets/screenshots/themes/theme-2.png" alt="Screenshot 2" width="200">\n<img src="readme-assets/screenshots/themes/theme-3.png" alt="Screenshot 3" width="200">\n</div>\n',
    'author': 'FredHappyface',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FHPythonUtils/CatPandoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
