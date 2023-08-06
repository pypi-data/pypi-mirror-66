# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bvill_apdft', 'bvill_apdft.tests']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'click>=7.1.1,<8.0.0']

entry_points = \
{'console_scripts': ['apdft = bvill_apdft.cli:run']}

setup_kwargs = {
    'name': 'bvill.apdft',
    'version': '0.1.0a0',
    'description': 'Another PDF Tool helps you quickly operate on PDF files with actions such as rotate, merging, and splitting via the command-line. Currently only supports merging.',
    'long_description': "Another PDF Tool\n================\n\nAnother PDF Tool helps you quickly operate on PDF files with actions such as rotate, \nmerging, and splitting pages from the command-line.\n\nThis project is in it's early stages of development, it currently only supports one \noperation.\n\nPlease stay tuned or open an issue or pull request if you'd like to help me out! I do\nhave a day job so I'm only working on this in my free time, development will likely be\nslow.\n\n**Table of Contents**\n- [Another PDF Tool](#another-pdf-tool)\n  - [Download](#download)\n  - [Usage](#usage)\n    - [Merge](#merge)\n  - [Author's Note](#authors-note)\n\nDownload\n--------\n**Requires Python 3.6 or higher.** I am investigating packaging options for end users\nwithout needing Python to be pre-installed.\n\nYou can clone this repository and build it yourself with\n[`poetry`](https://python-poetry.org/docs/), or get it with `pip`. If you are\ndownloading it I'll assume you already know how to use Python modules, and `pip`, \nspecifically on your operating system.\n\n```terminal\npython -m pip install bvill.apdft --user\n```\n\nWhy `bvill.apdft`? Because just `apdft` [is already taken](https://pypi.org/project/apdft/) :(\nFormally this project should be known as *Another PDF Tool* or `apdft` to refer to the\ncommand-line script name.\n\nUsage\n-----\n\nAt the moment, the only operation supported is to merge multiple `.pdf` files into one.\nMore is on its way :)\n\nRun the application in the terminal emulator of your choice.\n\n```terminal\napdft --version\napdft --help\napdft merge --help\n```\n\n### Merge\n\nThe PDF files will be merged in the same order they are specified in the source arguments\n\nYou can specify multiple `.pdf` files to merge into one output file\n\n```terminal\napdft path/to/your/file1.pdf path/to/your/file2.pdf path/to/out.pdf\n```\n\nYou can also specify directories containing `.pdf` files as your source input\n\n```terminal\napdft path/to/your/file1.pdf path/to/dir/with/pdfs path/to/out.pdf\n```\n\nBy default if one or more of your sources is a directory, then it is searched\nrecursively until all `.pdf` files are found. Then it will sort all `.pdf` files\nalphanumerically by their filenames. Sorting only occurs at the position where the \ndirectory is specified.\n\nFor example, imagine this is the contents of `./dir`:\n\n```\n./dir\n|-- 0\n|   `-- 3.pdf\n|-- 1.pdf\n`-- 2.pdf\n```\n\nIf you run `apdft merge` like this:\n\n```terminal\napdft merge b.pdf dir a.pdf dest.pdf\n```\n\nThe result will effectively be calling it like this:\n\n```terminal\napdft merge b.pdf dir/1.pdf dir/2.pdf dir/0/3.pdf a.pdf dest.pdf\n````\n\nYou can disable this behavior with the `-d` flag, and it will default to the natural\nsearch order defined by the OS (`os.listdir`). Note that this will still not change\nthe position of the SRC argument when it is a directory.\n\nAuthor's Note\n-------------\nFirst and foremost, this project is intended to be a learning exercise in developing,\npackaging, and distributing a modern Python-based desktop GUI application. That has been\nmy goal since the beginning, but I decided I should take an *Agile* approach by delivering\nsmall, incremental releases to the public. Although the project is still in it's initial\ndevelopment stage, this will help set the foundation for a consistent release cycle if I\ndecide to do more with it in the future.\n\nThe concept for *Another PDF Tool* came to me because I realized that often I need to\nquickly concatenate multiple PDF files together, or to break one up into seperate files.\nOf course I'm aware that there are a ton of free online PDF tools that do this already\n(seriously, just go to Google and search *PDF Tool*). But whenever I would use one of \nthose I always had a nagging feeling that my data was not kept private, which is mostly\na concern only when my PDF files contain sensitive personal information. It's also \nsurprising that the most common, free PDF viewing tools don't support the functionality \nI desire. Regardless, an open source desktop PDF editing tool sounded like a great \nfirst Python project to do on the weekends, that is not just an ad-hoc script of sorts.\n\nMy idea is to write out an uncomplicated backend utilizing the PyPDF2 library and\nbuild on top of it by first creating a stupidly-simple command-line interface, then a \nGUI for the primary end-userbase with something like wxPython or Electron, and possibly \na HTTP REST API which might be a requirement for an Electron or other web-based frontend\n`anyway.",
    'author': 'Brandon Villagran',
    'author_email': 'bvillagran.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
