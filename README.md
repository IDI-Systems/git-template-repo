# git-template-repo

[![CI - Test](https://github.com/IDI-Systems/git-template-repo/actions/workflows/test.yml/badge.svg)](https://github.com/IDI-Systems/git-template-repo/actions/workflows/test.yml)
[![CI - Build](https://github.com/IDI-Systems/git-template-repo/actions/workflows/build.yml/badge.svg)](https://github.com/IDI-Systems/git-template-repo/actions/workflows/build.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/git-template-repo.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/git-template-repo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/git-template-repo.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/git-template-repo)

A Python script that automates a 30-second task but is annoying to remember the exact steps.

Template repositories are very useful for quick-starting new projects and ensuring they start with the appropriate configuration for your team. Git services such as GitHub and GitLab offer "template repositories" that let users generate new repositories from a specified template. git-template-repo brings this feature to command-line git, allowing creation of new repositories from any accessible repository.

Some use cases include:
- Template repositories locally.
- Template repositories on free versions of GitLab or other git services.
- Template repositories in automated processes.
- Template repositories from submodules.


## Installation

git-template-repo is distributed on [PyPI](https://pypi.org/).

```
$ pip install git-template-repo
```
_Note: Add pip installation directory to `PATH` environmental variable to use it directly._

Alternatively install from source in this directory

```
$ pip install .
```


## Usage

If installed via `pip`, then should be available as a `git` command.

```sh
git template-repo new_repo_url template_repo_url

# Template remote repository
$ git template-repo jsonjsc-new https://github.com/IDI-Systems/jsonjsc
$ git template-repo jsonjsc-new https://gitlab.com/gitlab-org/gitlab-runner
# from different remote repository branch
$ git template-repo jsonjsc-new https://github.com/pypa/pip --template-branch main

# Template local repository
$ git template-repo jsonjsc-new ../jsonjsc
# from specific local repository commit
$ git template-repo jsonjsc-new ../jsonjsc --template-branch f0474566d698d6d70fe1c9b7cfd63a20f3a90aa7

# Template remote repository (jsonjsc) into another remote repository (jsonjsc-new, local clone will be created)
$ git template-repo https://github.com/IDI-Systems/jsonjsc-new https://github.com/IDI-Systems/jsonjsc
# with named local clone (new-jsonjsc, otherwise remote name is used)
$ git template-repo https://github.com/IDI-Systems/jsonjsc-new https://github.com/IDI-Systems/jsonjsc --clone-dir new-jsonjsc
# with push (back to target remote repository)
$ git template-repo https://github.com/IDI-Systems/jsonjsc-new https://github.com/IDI-Systems/jsonjsc --push
```

```
usage: git-template-repo [-h] [--new-root NEW_ROOT]
                         [--template-branch TEMPLATE_BRANCH] [--clone-dir CLONE_DIR]
                         [--no-clone] [--push] [--origin ORIGIN] [--clean-up] [-v]
                         new_repo template_repo

Git Template Script - Populates another repository with a commit from an existing repository.

positional arguments:
  new_repo              URL or file location of the new repository you wish to initialize the
                        template in. Note: if the path is a remote repository you can specify
                        the name of the local folder to clone into with --clone-dir, if the path
                        is local, then this is the folder where the repo will be initialized and
                        --clone-dir is redundant. If --push is set and the path is local, it is
                        assumed to be a git repository and is handled as a remote repository.
  template_repo         Local or remote repository in which to clone the template from.

options:
  -h, --help            show this help message and exit
  --new-root NEW_ROOT   Name of the root branch created in the new repository (default: master).
  --template-branch TEMPLATE_BRANCH
                        Name of the branch or SHA1 of the commit to clone from the template
                        repository (default: master).
  --clone-dir CLONE_DIR
                        Name of folder to clone into, by default will be the name of the remote
                        repository. Redundant if the new_repo is local.
  --no-clone            If set and the new_repo is remote this will not clone the remote path
                        specified as the template destination, but will initialize a new
                        repository. Still follows all folder naming rules of --clone-dir.
                        If set --push has no effect and will not push due to unknown state of
                        remote repository.
  --push                If set, once completed this will push the changes to the new remote
                        repository. If set new_repo is assumed to be a git repository.
  --origin ORIGIN       Name of origin remote to push to if --push is set (default: origin).
  --clean-up            If set, will remove repository. Useful for automated scripts that are
                        simply applying a template during CI or some other automated task.
  -v, --version         show version
```


## Development

git-template-repo uses [Hatchling](https://hatch.pypa.io/latest/) as a build backend and [flake8](https://flake8.pycqa.org/en/latest/) as a style guide.

```
$ pip install -e .
```

[Hatch](https://hatch.pypa.io/latest/) is the primary project manager of choice, but any project adhering to PEP 621 (`pyproject.toml` specification) can be used.

```
$ hatch shell
```

### Tests

Tests can be ran with [pytest](https://docs.pytest.org/). Hatch scripts are included for linting and testing.

```
# Lint
$ hatch run lint:all

# Test with current Python version
$ hatch run full
# Test with all Python versions
$ hatch run test:full
```
