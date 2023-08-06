# python validating types (vtypes)

*Validating types for python - use `isinstance()` to validate both type and value.*

[![Python versions](https://img.shields.io/pypi/pyversions/vtypes.svg)](https://pypi.python.org/pypi/vtypes/) [![Build Status](https://travis-ci.org/smarie/python-vtypes.svg?branch=master)](https://travis-ci.org/smarie/python-vtypes) [![Tests Status](https://smarie.github.io/python-vtypes/junit/junit-badge.svg?dummy=8484744)](https://smarie.github.io/python-vtypes/junit/report.html) [![codecov](https://codecov.io/gh/smarie/python-vtypes/branch/master/graph/badge.svg)](https://codecov.io/gh/smarie/python-vtypes)

[![Documentation](https://img.shields.io/badge/doc-latest-blue.svg)](https://smarie.github.io/python-vtypes/) [![PyPI](https://img.shields.io/pypi/v/vtypes.svg)](https://pypi.python.org/pypi/vtypes/) [![Downloads](https://pepy.tech/badge/vtypes)](https://pepy.tech/project/vtypes) [![Downloads per week](https://pepy.tech/badge/vtypes/week)](https://pepy.tech/project/vtypes) [![GitHub stars](https://img.shields.io/github/stars/smarie/python-vtypes.svg)](https://github.com/smarie/python-vtypes/stargazers)

**TODO a few lines to describe**

**This is the readme for developers.** The documentation for users is available here: [https://smarie.github.io/python-vtypes/](https://smarie.github.io/python-vtypes/)

## Want to contribute ?

Contributions are welcome ! Simply fork this project on github, commit your contributions, and create pull requests.

Here is a non-exhaustive list of interesting open topics: [https://github.com/smarie/python-vtypes/issues](https://github.com/smarie/python-vtypes/issues)

## Installing all requirements

In order to install all requirements, including those for tests and packaging, use the following command:

```bash
pip install -r ci_tools/requirements-pip.txt
```

## Running the tests

This project uses `pytest`.

```bash
pytest -v vtypes/tests/
```

## Packaging

This project uses `setuptools_scm` to synchronise the version number. Therefore the following command should be used for development snapshots as well as official releases: 

```bash
python setup.py egg_info bdist_wheel rotate -m.whl -k3
```

## Generating the documentation page

This project uses `mkdocs` to generate its documentation page. Therefore building a local copy of the doc page may be done using:

```bash
mkdocs build -f docs/mkdocs.yml
```

## Generating the test reports

The following commands generate the html test report and the associated badge. 

```bash
pytest --junitxml=junit.xml -v vtypes/tests/
ant -f ci_tools/generate-junit-html.xml
python ci_tools/generate-junit-badge.py
```

### PyPI Releasing memo

This project is now automatically deployed to PyPI when a tag is created. Anyway, for manual deployment we can use:

```bash
twine upload dist/* -r pypitest
twine upload dist/*
```

### Merging pull requests with edits - memo

Ax explained in github ('get commandline instructions'):

```bash
git checkout -b <git_name>-<feature_branch> master
git pull https://github.com/<git_name>/python-vtypes.git <feature_branch> --no-commit --ff-only
```

if the second step does not work, do a normal auto-merge (do not use **rebase**!):

```bash
git pull https://github.com/<git_name>/python-vtypes.git <feature_branch> --no-commit
```

Finally review the changes, possibly perform some modifications, and commit.
