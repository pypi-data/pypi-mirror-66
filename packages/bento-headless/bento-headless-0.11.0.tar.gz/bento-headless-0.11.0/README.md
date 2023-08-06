<h3 align="center">
  [alpha] A Git-aware CLI for running semgrep patterns in the developer and CI workflow.
</h3>

<p align="center">
  <a href="#installation">Installation</a>
  <span> · </span>
  <a href="#usage">Usage</a>
  <span> · </span>
  <a href="#help-and-community">Help & Community</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/bento-cli/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/bento-cli?style=flat-square&color=blue">
  </a>
  <a href="https://pypi.org/project/bento-cli/">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/bento-cli?style=flat-square&color=green">
  </a>
  <a href="https://github.com/returntocorp/bento/issues/new/choose">
    <img src="https://img.shields.io/badge/issues-welcome-green?style=flat-square" alt="Issues welcome!" />
  </a>
  <a href="https://twitter.com/intent/follow?screen_name=r2cdev">
    <img src="https://img.shields.io/twitter/follow/r2cdev?label=Follow%20r2cdev&style=social&color=blue" alt="Follow @r2cdev" />
  </a>
</p>

## Installation

Requires [Python 3.6+](https://www.python.org/downloads/) and [Docker 19.03+](https://docs.docker.com/get-docker/). It runs on macOS and Linux.

In a Git project directory:

```bash
$ pip3 install bento-headless
```

## Usage

### Upgrading

```bash
$ pip3 install --upgrade bento-headless
```

### Command line options

```
$ bentoh --help
Usage: bentoh [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.
  --version   Show the version and exit.

Commands:
  archive  Suppress current findings.
  check    Checks for new findings.

  To get help for a specific command, run `bentoh COMMAND --help`
```

### Run custom `semgrep` checks on staged diffs

See [semgrep Configuration](https://github.com/returntocorp/semgrep/blob/develop/docs/config/advanced.md) for how to write custom rule files

```
vi .bento/semgrep.yml
bentoh check
```

### Format output as JSON

```
bentoh check -f json
```

### Run on file system current state

```
bentoh check --all
```

### Run on staged diffs in a directory

```
bentoh check src
```

### Ignore current findings

```
bentoh archive
```

### Run public semgrep checks on staged diffs

```
BENTO_REGISTRY=r/r2c.python bentoh check
```

### Run checks from extensions

```
bentoh check -t gosec -t r2c.registry.latest
```

### Exit codes

`bentoh check` may exit with the following exit codes:

- `0`: Bento ran successfully and found no errors
- `2`: Bento ran successfully and found issues in your code
- `3`: Bento or one of its underlying tools failed to run

## Extensions

`bentoh` ships with the following extensions:

| Extension           | Description                                                                           |
| ------------------- | ------------------------------------------------------------------------------------- |
| bandit              | Finds common security issues in Python code                                           |
| dlint               | A tool for encouraging best coding practices and helping ensure Python code is secure |
| eslint              | Identifies and reports on patterns in JavaScript and TypeScript                       |
| flake8              | Finds common bugs in Python code                                                      |
| gosec               | Finds security bugs in Go code                                                        |
| hadolint            | Finds bugs in Docker files (requires Docker)                                          |
| r2c.boto3           | Checks for the AWS boto3 library in Python                                            |
| r2c.flask           | Checks for the Python Flask framework                                                 |
| r2c.jinja           | Finds common security issues in Jinja templates                                       |
| r2c.registry.latest | Runs checks from r2c's check registry (experimental; requires Docker)                 |
| r2c.requests        | Checks for the Python Requests framework                                              |
| shellcheck          | Finds bugs in shell scripts (requires Docker)                                         |

## Help and community

Need help or want to share feedback? We’d love to hear from you!

- Email us at [support@r2c.dev](mailto:support@r2c.dev)
- Join #general in our [community Slack](https://join.slack.com/t/r2c-community/shared_invite/enQtNjU0NDYzMjAwODY4LWE3NTg1MGNhYTAwMzk5ZGRhMjQ2MzVhNGJiZjI1ZWQ0NjQ2YWI4ZGY3OGViMGJjNzA4ODQ3MjEzOWExNjZlNTA)
- [File an issue](https://github.com/returntocorp/bento/issues/new?assignees=&labels=bug&template=bug_report.md&title=) or [submit a feature request](https://github.com/returntocorp/bento/issues/new?assignees=&labels=feature-request&template=feature_request.md&title=) directly on GitHub

We’re constantly shipping new features and improvements.

## License and legal

Please refer to the [terms and privacy document](https://github.com/returntocorp/bento/blob/master/PRIVACY.md).

</br>
</br>
<p align="center">
    <img src="https://web-assets.r2c.dev/r2c-logo-silhouette.png?gh" height="24" alt="r2c logo"/>
</p>
<p align="center">
    Copyright (c) <a href="https://r2c.dev">r2c</a>.
</p>
