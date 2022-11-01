import os
import unittest

from git_template_repo import git_template_repo


class UnitTests(unittest.TestCase):
    def test_is_sha1_valid(self):
        self.assertTrue(git_template_repo.is_sha1("92229240f4172b921d76ce3fdaabc136dde4cde0"))

    def test_is_sha1_invalid_len(self):
        self.assertFalse(git_template_repo.is_sha1("92229240f4172b921d76ce3fdaabc136dde4cde"))

    def test_is_sha1_invalid_char(self):
        self.assertFalse(git_template_repo.is_sha1("92229240f4172b921d76ce3fdaabc136dde4cdeö"))

    def test_git_call(self):
        output = git_template_repo.make_call("git", "--version")
        self.assertIn(b"git version ", output)

    def test_git_rev_parse_head(self):
        sha = git_template_repo.make_call("git", "rev-parse", "--verify", "HEAD").decode()[:-1]
        self.assertTrue(git_template_repo.is_sha1(sha))
