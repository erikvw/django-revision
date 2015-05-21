from git import Repo, GitDB, InvalidGitRepositoryError

from django.conf import settings
from django.test.testcases import TestCase

from ..revision import site_revision, Revision


class TestRevision(TestCase):

    def test_revision(self):
        repo = Repo(settings.BASE_DIR.ancestor(1), odbt=GitDB)
        tag = repo.git.describe(tags=True)
        self.assertEquals(tag, site_revision.tag)

    def test_working_dir(self):
        DIR = '/tmp'
        self.assertRaises(InvalidGitRepositoryError, Repo, DIR, odbt=GitDB)
        revision = Revision(working_dir=DIR)
        self.assertRaises(InvalidGitRepositoryError, getattr, revision, 'revision')

    def test_manual_revision1(self):
        """Assert the django_revision can be set manually."""
        revision = Revision(manual_revision='0.1.0')
        self.assertEqual(revision.revision, '0.1.0')

    def test_manual_revision2(self):
        """Assert the django_revision can be set manually and a working_dir is ignored."""
        revision = Revision(manual_revision='0.1.0', working_dir='/tmp')
        self.assertEqual(revision.revision, '0.1.0')
