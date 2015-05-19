from git import Repo, GitDB, GitCommandError

from django.conf import settings
from django.test.testcases import TestCase

from revision import site_revision


class TestRevision(TestCase):

    def test_revision(self):
        repo = Repo(settings.BASE_DIR.ancestor(1), odbt=GitDB)
        tag = repo.git.describe(tags=True)
        self.assertEquals(tag, site_revision.tag)
