# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['failprint']

package_data = \
{'': ['*']}

install_requires = \
['ansimarkup>=1.4.0,<2.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'ptyprocess>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['failprint = failprint.cli:main']}

setup_kwargs = {
    'name': 'failprint',
    'version': '0.1.0',
    'description': 'Print only on failure.',
    'long_description': "# failprint\n\nPrint only on failure.\n\n*:warning: Work in progress!*\n\nTired of searching the `quiet` options of your programs\nto lighten up the output of your `make check` or `make lint` commands?\n\nTired of finding out that standard output and error are mixed up in some of them?\n\nSimply run your command through `failprint`.\nIf it succeeds, nothing is printed.\nIf it fails, standard error is printed.\nPlus other configuration goodies :wink:\n\n## Example\n\nSome tools output a lot of things. You don't want to see it when the command succeeds.\n\nWithout `failprint`:\n\n- `poetry run bandit -s B404 -r src/`\n- `poetry run black --check $(PY_SRC)`\n\n![basic](https://user-images.githubusercontent.com/3999221/79385294-a2a0e080-7f68-11ea-827d-f72134a02eef.png)\n\nWith `failprint`:\n\n- `poetry run failprint -- bandit -s B404 -r src/`\n- `poetry run failprint -- black --check $(PY_SRC)`\n\n![failprint_fail](https://user-images.githubusercontent.com/3999221/79385302-a5033a80-7f68-11ea-98cd-1f4148629724.png)\n\nIt's already better, no? Much more readable!\n\nAnd when everything passes, it's even better:\n\n![failprint_success](https://user-images.githubusercontent.com/3999221/79385308-a59bd100-7f68-11ea-8012-90cbe9e0ac08.png)\n\n## Usage\n\n```\nusage: failprint [-h] [-f {custom,pretty,tap}] [-o {stdout,stderr,combine}] [-n NUMBER] [-t TITLE] COMMAND [COMMAND ...]\n\npositional arguments:\n  COMMAND\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -f {custom,pretty,tap}, --format {custom,pretty,tap}\n                        Output format. Pass your own Jinja2 template as a string with '-f custom=TEMPLATE'.\n                        Available variables: title (command or title passed with -t), code (exit status), success (boolean), failure (boolean),\n                        n (command number passed with -n), output (command output). Available filters: indent (textwrap.indent).\n  -o {stdout,stderr,combine}, --output {stdout,stderr,combine}\n                        Which output to use. Colors are supported with 'combine' only, unless the command has a 'force color' option.\n  -n NUMBER, --number NUMBER\n                        Command number. Useful for the 'tap' format.\n  -t TITLE, --title TITLE\n                        Command title. Default is the command itself.\n```\n",
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawamoy/failprint',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
