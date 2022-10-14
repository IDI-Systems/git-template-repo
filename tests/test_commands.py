import unittest

from git_template_repo import git_template_repo


class UnitTests(unittest.TestCase):

    def test_call(self):
        output = git_template_repo.make_call("git", "--version")
        self.assertIn(b"git version ", output)


if __name__ == "__main__":
    unittest.main()
