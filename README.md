# git-template-repo

A python script that automates a 30-second task but is annoying to remember the exact steps.


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

```
git template-repo new_repo_url template_repo_url
```

```
usage: git-template-repo [-h] [--new-root NEW_ROOT]
                         [--template-branch TEMPLATE_BRANCH] [--clone-dir CLONE_DIR]
                         [--no-clone] [--push] [--origin ORIGIN] [--clean-up]
                         new_repo template_repo

Git Template Script - Populates another repository with a commit from an existing
repository.

positional arguments:
  new_repo              The URL or file location of the new repository you wish to
                        initialize the template in. Note: if the path is a remote
                        repository you can specify the name of the local folder to
                        clone into with --clone-dir, if the path is local, then this
                        is the folder where the repo will be initialized and
                        --clone-dir is redundant.
  template_repo         The local or remote repository in which to clone the
                        template from.

optional arguments:
  -h, --help            show this help message and exit
  --new-root NEW_ROOT   The name of the root branch created in the new repository.
                        Default=master
  --template-branch TEMPLATE_BRANCH
                        The name of the branch to clone from the template
                        repository. Default=master
  --clone-dir CLONE_DIR
                        Name of folder to clone into, by default will be the name of
                        the remote repository. Redundant if the new_repo is local.
  --no-clone            If set and the new_repo is remote this will not clone the
                        remote path specified as the template destination, but will
                        initialize a new repository. Still follows all folder naming
                        rules of --clone-dir. If set --push has no effect and will
                        not push due to unknown state of remote repository.
  --push                If set, once completed this will push the changes to the new
                        remote repository.
  --origin ORIGIN       Name of origin remote to push to if --push is set.
                        Default=origin
  --clean-up            If set, will remove repository. Useful for automated scripts
                        that are simply applying a template during CI or some other
                        automated task.
  -v, --version         show version
```


## Development

git-template-repo uses [Hatchling](https://hatch.pypa.io/latest/) as a build backend and [tox](https://tox.wiki/en/latest/) for automation and [flake8](https://flake8.pycqa.org/en/latest/) as a style guide.

```
$ pip install -e .
```

[Hatch](https://hatch.pypa.io/latest/) is the primary project manager of choice, but any project adhering to PEP 621 (`pyproject.toml` specification) can be used.

```
$ hatch shell
```

### Tests

Tests can be ran with [pytest](https://docs.pytest.org/en/7.1.x/). Hatch scripts are included as well and will run `pytest` as well as `flake8`.

```
# Current Python version
$ hatch run test
# All Python versions
$ hatch run test:test
```
