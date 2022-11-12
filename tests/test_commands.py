import os
import shutil
import sys
import unittest
from pathlib import Path

from git_template_repo import git_template_repo

TEST_REPO_DIR = Path("./test-repo")
TEST_REPO_URL = "https://github.com/IDI-Systems/git-template-repo"
TEST_REPO_DIR_GIT = TEST_REPO_DIR / ".git"
TEST_DIR = Path("./test-dir")


class UnitTests(unittest.TestCase):
    def tearDown(self):
        if TEST_REPO_DIR.exists():
            shutil.rmtree(TEST_REPO_DIR, onerror=git_template_repo.onerror)
        if TEST_DIR.exists():
            shutil.rmtree(TEST_DIR, onerror=git_template_repo.onerror)

    def assertIsDir(self, path):
        if not path.is_dir():
            raise AssertionError(f"Directory does not exist: {path}")

    def assertIsNotDir(self, path):
        if path.is_dir():
            raise AssertionError(f"Directory exist: {path}")

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_rmtree_onerror(self):
        TEST_DIR.mkdir()
        (TEST_DIR / "test-readonly").touch(mode=0o000)
        with self.assertRaises(OSError):
            shutil.rmtree(TEST_DIR)
        shutil.rmtree(TEST_DIR, onerror=git_template_repo.onerror)
        self.assertIsNotDir(TEST_DIR)

    def test_help(self):
        sys.argv = ["git-template-repo", "-h"]
        with self.assertRaises(SystemExit):
            git_template_repo.main()

    def test_template_from_url(self):
        sys.argv = ["git-template-repo", str(TEST_REPO_DIR), TEST_REPO_URL]
        ret = git_template_repo.main()
        self.assertEqual(ret, 0)
        self.assertIsDir(TEST_REPO_DIR)
        self.assertIsDir(TEST_REPO_DIR_GIT)
        self.assertEqual(int(git_template_repo.make_call("git", "--git-dir", str(TEST_REPO_DIR_GIT), "rev-list", "--all", "--count")), 1)

    def test_template_from_local_branch(self):
        ci = os.environ.get("CI", False)
        if ci:
            git_template_repo.make_call("git", "checkout", "-b", "test-master")

        sys.argv = ["git-template-repo", str(TEST_REPO_DIR), str(Path.cwd()), "--template-branch", "test-master" if ci else "master"]
        ret = git_template_repo.main()
        self.assertEqual(ret, 0)
        self.assertIsDir(TEST_REPO_DIR)
        self.assertIsDir(TEST_REPO_DIR_GIT)
        self.assertEqual(int(git_template_repo.make_call("git", "--git-dir", str(TEST_REPO_DIR_GIT), "rev-list", "--all", "--count")), 1)

    def test_template_from_local_commit(self):
        sha = git_template_repo.make_call("git", "rev-parse", "--verify", "HEAD").decode()[:-1]
        sys.argv = ["git-template-repo", str(TEST_REPO_DIR), str(Path.cwd()), "--template-branch", sha]
        ret = git_template_repo.main()
        self.assertEqual(ret, 0)
        self.assertIsDir(TEST_REPO_DIR)
        self.assertIsDir(TEST_REPO_DIR_GIT)
        self.assertEqual(int(git_template_repo.make_call("git", "--git-dir", str(TEST_REPO_DIR_GIT), "rev-list", "--all", "--count")), 1)

    def test_template_on_existing_dir(self):
        TEST_REPO_DIR.mkdir()
        sys.argv = ["git-template-repo", str(TEST_REPO_DIR), str(Path.cwd())]
        ret = git_template_repo.main()
        self.assertEqual(ret, 1)
        self.assertIsDir(TEST_REPO_DIR)
        self.assertIsNotDir(TEST_REPO_DIR_GIT)
