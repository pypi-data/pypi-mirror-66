# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bento',
 'bento.commands',
 'bento.content',
 'bento.extra',
 'bento.formatter',
 'bento.tool',
 'bento.tool.runner']

package_data = \
{'': ['*'], 'bento': ['configs/*'], 'bento.extra': ['eslint/*']}

install_requires = \
['PyYAML>=5.1.2',
 'attrs>=18.2.0,<=19.3.0',
 'click>=7.0,<8.0',
 'docker>=3.7,<4.0',
 'frozendict>=1.2,<2.0',
 'gitpython>=2.1,<3.0',
 'packaging>=14.0',
 'pre-commit>=1.0.0,<=1.18.3',
 'psutil>=5.6.3,<5.7.0',
 'pymmh3>=0.0.5,<0.1.0',
 'semantic-version>=2.8.0,<2.9.0',
 'tqdm>=4.36.1,<4.37.0',
 'validate-email>=1.3,<2.0']

entry_points = \
{'console_scripts': ['bentoh = bento.__main__:headless']}

setup_kwargs = {
    'name': 'bento-headless',
    'version': '0.11.0',
    'description': 'Git-aware utility for automated program analysis',
    'long_description': '<h3 align="center">\n  [alpha] A Git-aware CLI for running semgrep patterns in the developer and CI workflow.\n</h3>\n\n<p align="center">\n  <a href="#installation">Installation</a>\n  <span> · </span>\n  <a href="#usage">Usage</a>\n  <span> · </span>\n  <a href="#help-and-community">Help & Community</a>\n</p>\n\n<p align="center">\n  <a href="https://pypi.org/project/bento-cli/">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/bento-cli?style=flat-square&color=blue">\n  </a>\n  <a href="https://pypi.org/project/bento-cli/">\n    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/bento-cli?style=flat-square&color=green">\n  </a>\n  <a href="https://github.com/returntocorp/bento/issues/new/choose">\n    <img src="https://img.shields.io/badge/issues-welcome-green?style=flat-square" alt="Issues welcome!" />\n  </a>\n  <a href="https://twitter.com/intent/follow?screen_name=r2cdev">\n    <img src="https://img.shields.io/twitter/follow/r2cdev?label=Follow%20r2cdev&style=social&color=blue" alt="Follow @r2cdev" />\n  </a>\n</p>\n\n## Installation\n\nRequires [Python 3.6+](https://www.python.org/downloads/) and [Docker 19.03+](https://docs.docker.com/get-docker/). It runs on macOS and Linux.\n\nIn a Git project directory:\n\n```bash\n$ pip3 install bento-headless\n```\n\n## Usage\n\n### Upgrading\n\n```bash\n$ pip3 install --upgrade bento-headless\n```\n\n### Command line options\n\n```\n$ bentoh --help\nUsage: bentoh [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -h, --help  Show this message and exit.\n  --version   Show the version and exit.\n\nCommands:\n  archive  Suppress current findings.\n  check    Checks for new findings.\n\n  To get help for a specific command, run `bentoh COMMAND --help`\n```\n\n### Run custom `semgrep` checks on staged diffs\n\nSee [semgrep Configuration](https://github.com/returntocorp/semgrep/blob/develop/docs/config/advanced.md) for how to write custom rule files\n\n```\nvi .bento/semgrep.yml\nbentoh check\n```\n\n### Format output as JSON\n\n```\nbentoh check -f json\n```\n\n### Run on file system current state\n\n```\nbentoh check --all\n```\n\n### Run on staged diffs in a directory\n\n```\nbentoh check src\n```\n\n### Ignore current findings\n\n```\nbentoh archive\n```\n\n### Run public semgrep checks on staged diffs\n\n```\nBENTO_REGISTRY=r/r2c.python bentoh check\n```\n\n### Run checks from extensions\n\n```\nbentoh check -t gosec -t r2c.registry.latest\n```\n\n### Exit codes\n\n`bentoh check` may exit with the following exit codes:\n\n- `0`: Bento ran successfully and found no errors\n- `2`: Bento ran successfully and found issues in your code\n- `3`: Bento or one of its underlying tools failed to run\n\n## Extensions\n\n`bentoh` ships with the following extensions:\n\n| Extension           | Description                                                                           |\n| ------------------- | ------------------------------------------------------------------------------------- |\n| bandit              | Finds common security issues in Python code                                           |\n| dlint               | A tool for encouraging best coding practices and helping ensure Python code is secure |\n| eslint              | Identifies and reports on patterns in JavaScript and TypeScript                       |\n| flake8              | Finds common bugs in Python code                                                      |\n| gosec               | Finds security bugs in Go code                                                        |\n| hadolint            | Finds bugs in Docker files (requires Docker)                                          |\n| r2c.boto3           | Checks for the AWS boto3 library in Python                                            |\n| r2c.flask           | Checks for the Python Flask framework                                                 |\n| r2c.jinja           | Finds common security issues in Jinja templates                                       |\n| r2c.registry.latest | Runs checks from r2c\'s check registry (experimental; requires Docker)                 |\n| r2c.requests        | Checks for the Python Requests framework                                              |\n| shellcheck          | Finds bugs in shell scripts (requires Docker)                                         |\n\n## Help and community\n\nNeed help or want to share feedback? We’d love to hear from you!\n\n- Email us at [support@r2c.dev](mailto:support@r2c.dev)\n- Join #general in our [community Slack](https://join.slack.com/t/r2c-community/shared_invite/enQtNjU0NDYzMjAwODY4LWE3NTg1MGNhYTAwMzk5ZGRhMjQ2MzVhNGJiZjI1ZWQ0NjQ2YWI4ZGY3OGViMGJjNzA4ODQ3MjEzOWExNjZlNTA)\n- [File an issue](https://github.com/returntocorp/bento/issues/new?assignees=&labels=bug&template=bug_report.md&title=) or [submit a feature request](https://github.com/returntocorp/bento/issues/new?assignees=&labels=feature-request&template=feature_request.md&title=) directly on GitHub\n\nWe’re constantly shipping new features and improvements.\n\n## License and legal\n\nPlease refer to the [terms and privacy document](https://github.com/returntocorp/bento/blob/master/PRIVACY.md).\n\n</br>\n</br>\n<p align="center">\n    <img src="https://web-assets.r2c.dev/r2c-logo-silhouette.png?gh" height="24" alt="r2c logo"/>\n</p>\n<p align="center">\n    Copyright (c) <a href="https://r2c.dev">r2c</a>.\n</p>\n',
    'author': 'Return To Corporation',
    'author_email': 'hello@r2c.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://bento.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
