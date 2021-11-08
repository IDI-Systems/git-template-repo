# git-template-repo

A python script that automates a 30-second task but is annoying to remember the exact steps.

## Install

Eventually on PyPi.

Otherwise run setup.py.

## Usage

If installed via setup.py or pip, then should be available as a `git` command.

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
```
