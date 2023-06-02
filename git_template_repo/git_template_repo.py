import argparse
import os
import re
import shutil
import subprocess
import sys

from ._version import version as __version__


def make_call(*args, error_msg=None, suppress_output=True):
    try:
        output = subprocess.check_output(args)
        if not suppress_output:
            print(output.decode("utf-8"), end="")

        return output

    except Exception as e:
        if error_msg:
            print(error_msg)
            print("")
        print(e)
        raise e


def is_sha1(sha):
    match = re.match(r'\b[0-9a-f]{40}\b', sha)
    return match is not None


def execute(args):
    new_repo = args.new_repo
    template_repo = args.template_repo

    clone_dir = args.clone_dir
    new_root_branch = args.new_root
    no_clone = args.no_clone

    push_origin = args.push
    origin_name = args.origin

    template_branch = args.template_branch

    make_call("git", "--version",
              error_msg=("ERROR: Could not find git on the path, please make sure git is installed and available in "
                         "the path environment."),
              suppress_output=False)

    local_new = True
    if push_origin or "https://" in new_repo or "http://" in new_repo or "ssh://" in new_repo:
        local_new = False

    if local_new:
        clone_dir = new_repo
        if not os.path.exists(clone_dir):
            os.makedirs(clone_dir)
        else:
            print("ERROR: Repository directory already exists.")
            return 1
        os.chdir(clone_dir)
        make_call("git", "init")

    else:
        if not clone_dir:
            folders = os.path.split(new_repo)
            if folders:
                clone_dir = folders[-1]
                if ".git" == clone_dir[-4:]:
                    clone_dir = clone_dir[0:-4]
            else:
                print(f"ERROR: Cannot determine the appropriate folder name from the URL: {new_repo}")
                return 1

        if no_clone and not os.path.exists(clone_dir):
            os.makedirs(clone_dir)
        else:
            if os.path.exists(clone_dir):
                print("ERROR: Repository directory already exists.")
                return 1

        if no_clone:
            os.chdir(clone_dir)
            make_call("git", "init")
        else:
            make_call("git", "clone", "--no-tags", new_repo, clone_dir)
            os.chdir(clone_dir)

    if int(make_call("git", "rev-list", "--all", "--count")):
        print("ERROR: Can only initialize a template on an empty repository with no commits.")
        return 1

    make_call("git", "remote", "add", "template", template_repo)

    if is_sha1(template_branch):
        make_call("git", "fetch", "--no-tags", "template", template_branch)
        make_call("git", "checkout", "--orphan", new_root_branch, template_branch)
    else:
        make_call("git", "fetch", "--no-tags", "template")
        make_call("git", "checkout", "--orphan", new_root_branch, f"template/{template_branch}")

    make_call("git", "add", "-A")
    make_call("git", "commit", "-m", f"Template initialization from {template_repo}.")
    make_call("git", "remote", "rm", "template")
    if push_origin and not local_new and not no_clone:
        if origin_name != "origin":
            make_call("git", "remote", "add", origin_name, new_repo)
        make_call("git", "push", origin_name, f"{new_root_branch}:{new_root_branch}")
    else:
        if push_origin and no_clone:
            print("WARNING: Cannot push when flag --no-clone is set as state of remote repository in which template "
                  "was initialized is unknown.")

    return 0


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat

    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def main():
    parser = argparse.ArgumentParser(
        prog="git-template-repo",
        description=("Git Template Script - Populates another repository with a commit from an existing repository."))

    parser.add_argument(
        "new_repo", type=str,
        help="URL or file location of the new repository you wish to initialize the template in. Note: if the path is a remote repository you can specify the "
             "name of the local folder to clone into with --clone-dir, if the path is local, then this is the folder where the repo will be initialized and "
             "--clone-dir is redundant. If --push is set and the path is local, it is assumed to be a git repository and is handled as a remote repository.")
    parser.add_argument(
        "template_repo", type=str,
        help="Local or remote repository in which to clone the template from.")
    parser.add_argument(
        "--new-root", default="master", type=str,
        help="Name of the root branch created in the new repository (default: %(default)s).")
    parser.add_argument(
        "--template-branch", default="master", type=str,
        help="Name of the branch or SHA1 of the commit to clone from the template repository (default: %(default)s).")
    parser.add_argument(
        "--clone-dir", default="", type=str,
        help="Name of folder to clone into, by default will be the name of the remote repository. Redundant if the new_repo is local.")
    parser.add_argument(
        "--no-clone", action="store_true",
        help="If set and the new_repo is remote this will not clone the remote path specified as the template destination, but will initialize a new repository"
             ". Still follows all folder naming rules of --clone-dir. If set --push has no effect and will not push due to unknown state of remote repository.")
    parser.add_argument(
        "--push", action="store_true",
        help="If set, once completed this will push the changes to the new remote repository. If set new_repo is assumed to be a git repository.")
    parser.add_argument(
        "--origin", default="origin", type=str,
        help="Name of origin remote to push to if --push is set (default: %(default)s).")
    parser.add_argument(
        "--clean-up", action="store_true",
        help="If set, will remove repository. Useful for automated scripts that are simply applying a template during CI or some other automated task.")
    parser.add_argument("-v", "--version", action="store_true", help="show version")

    args = parser.parse_args()

    if args.version:
        print(f"git-template-repo v{__version__}")
        return 0

    cwdir = os.getcwd()

    ret = execute(args)

    if (ret == 0 and args.clean_up) or ret != 0:
        cleanup_dir = os.getcwd()
        if cleanup_dir != cwdir and (cwdir in cleanup_dir or cleanup_dir == args.clone_dir or cleanup_dir == args.new_repo):
            print("Cleaning up working directory: ", cleanup_dir)
            os.chdir(cwdir)
            shutil.rmtree(cleanup_dir, onerror=onerror)

    os.chdir(cwdir)

    return ret


if __name__ == "__main__":
    sys.exit(main())
