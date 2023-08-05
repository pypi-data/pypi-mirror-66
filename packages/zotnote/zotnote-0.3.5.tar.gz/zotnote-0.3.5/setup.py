# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zotnote',
 'zotnote.config',
 'zotnote.connectors',
 'zotnote.notes',
 'zotnote.utils']

package_data = \
{'': ['*'], 'zotnote.notes': ['templates/*', 'templates/content/*']}

install_requires = \
['click-option-group>=0.3.0,<0.4.0',
 'click>=7.1.1,<8.0.0',
 'jinja2>=2.11.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'tomlkit>=0.5.11,<0.6.0',
 'xdg>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['zotnote = zotnote.app:main']}

setup_kwargs = {
    'name': 'zotnote',
    'version': '0.3.5',
    'description': 'Streamlining reading notes with Zotero',
    'long_description': '# ZotNote\n\nAutomatize and manage your reading notes with Zotero & Better Bibtex Plugin (BBT). **Note: ZotNote is still in early development and not production ready**\n\n[![PyPI version](https://img.shields.io/pypi/v/zotnote.svg)](https://pypi.python.org/pypi/zotnote/)\n\n![ZotNote demo](assets/demo.gif)\n\n---\n\n*Current features*\n\n- Simple installation via pipx/pip\n- Full command-line interface to create, edit, and remove notes\n- Graphical interface to select a Zotero item\n- Support for various reading note templates\n\n*Planned features*\n\n- Annotation of reading notes and individual quotes using tags/keywords\n  - Retrieval of relevant quotes based on these tags and keywords\n  - Analytics based on these tags and keywords\n- Enrich reading notes with more metadata from Zotero\n- Simple reports about progress of literature review\n- (*dreaming*) Automatically export collection of notes as an annotated bibliography.\n\n*Long-term vision*\n\nA literature review suite that connects to Zotero & BBT. Management of reading notes, reading/writing analytics, and basic qualitative text analysis (export reports as HTML via Jupyter notebooks). Export of reading notes in different formats (e.g., annotated bibliography).\n\nYou can find a roadmap for ZotNote [here](https://github.com/Bubblbu/zotnote/issues/7).\n\n## Installation\n\n### Requirements\n\n- [Python](https://www.python.org/downloads/) 3.6 or higher\n- [Zotero Standalone](https://www.zotero.org/) with [Better Bibtex plugin](https://github.com/retorquere/zotero-better-bibtex)\n\n### Recommended: Install via pipx\n\nThe recommended way to install ZotNote is using [pipx](https://pipxproject.github.io/pipx/). Pipx cleanly install the package in an isolated environment (clean uninstalls!) and automagically exposes the CLI-endpoints globally on your system.\n\n    pipx install zotnote\n\n### Option 2: Install via pip\n\nHowever, you can also simply use pip. Please be aware of the Python version and environments you are using.\n\n    pip install zotnote\n\n### Option 3: Download from GitHub\n\nDownload the latest release from Github and unzip. Put the folder containing the scripts into your `PATH`.\n\nAlternatively, run\n\n\n    [sudo] python3 setup.py install\n\nor\n\n    python3 setup.py install --user\n\n### Option 4: Git clone (for developers)\n\n    git clone git@github.com:Bubblbu/zotnote.git\n\nThe project is being developed with [Poetry](https://python-poetry.org/) as a dependency manager.\n\nMore instructions will follow soon!\n\n## Getting started\n\n```\nUsage: zotnote [OPTIONS] COMMAND [ARGS]...\n\n  CLI for ZotNote.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  add        Create a new note.\n  config     Configure Zotnote from the command line.\n  edit       Open a note in your editor of choice.\n  remove     Remove a note\n  templates  List all available templates for notes.\n```\n\n### Configuration\n\nAfter installation you should be able to simply run `zotnote` and be prompted to a quick command-line configuration.\n\nZotNote currently asks you for:\n\n- A name which is used in all reading notes.\n- An email address\n- A folder to store your reading notes\n\n### Usage\n\nSome basic use cases:\n\nCreate a note with the graphical interface (Zotero picker)\n\n    zotnote add\n\nCreate for specific citekey\n\n    zotnote add [citekey]\n\nEdit a note (with graphical picker)\n\n    zotnote edit\n\nor\n\n    zotnote edit [citekey]\n\nYou can explore each command in detail by adding `--help`.\n\n## Authors\n\nWritten by [Asura Enkhbayar](https://twitter.com/bubblbu_) while he was quarantined.\n',
    'author': 'Asura Enkhbayar',
    'author_email': 'asura.enkhbayar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bubblbu/zotnote',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
