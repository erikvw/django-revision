from django.conf import settings
from django.test.testcases import TransactionTestCase
from django_revision import site_revision, Revision
from git import Repo, GitDB
from git.exc import InvalidGitRepositoryError

from .models import TestModel
from pathlib import Path


class TestRevision(TransactionTestCase):

    def setUp(self):
        path = str(Path(settings.BASE_DIR).parent)
        repo = Repo(path, odbt=GitDB)
        self.tag = str(repo.git.describe(tags=True))
        try:
            self.branch = str(repo.active_branch)
            self.commit = str(repo.active_branch.commit)
        except TypeError:
            self.branch = 'detached'
            self.commit = str(repo.commit())
        self.revision = '{}:{}:{}'.format(
            self.tag, self.branch, self.commit)[0: 75]

    def test_model(self):
        test_model = TestModel()
        test_model.save()
        self.assertEqual(test_model.revision_field, self.revision)
        test_model = TestModel.objects.create()
        self.assertEqual(test_model.revision_field, self.revision)

    def test_revision(self):
        path = str(Path(settings.BASE_DIR).parent)
        repo = Repo(path, odbt=GitDB)
        tag = repo.git.describe(tags=True)
        self.assertEquals(tag, site_revision.tag)

    def test_revision_branch(self):
        revision = Revision()
        self.assertEqual(revision.branch, self.branch)

    def test_revision_tag(self):
        revision = Revision()
        self.assertEqual(revision.tag, self.tag)

    def test_revision_commit(self):
        revision = Revision()
        self.assertEqual(revision.commit, self.commit)

    def test_working_dir(self):
        DIR = '/tmp'
        self.assertRaises(InvalidGitRepositoryError, Repo, DIR, odbt=GitDB)
        self.assertEqual(Revision(working_dir=DIR).revision, settings.REVISION)

    def test_manual_revision1(self):
        """Assert the django_revision does not set manually if repo can be found ."""
        revision = Revision(manual_revision='0.1.0')
        self.assertNotEqual('0.1.0', revision.revision)

    def test_manual_revision2(self):
        """Assert the django_revision can be set manually and a working_dir is ignored."""
        revision = Revision(manual_revision='0.1.0', working_dir='/tmp')
        self.assertEqual(revision.revision, '0.1.0')
