from tempfile import mkdtemp
from unittest.case import skip

from django.conf import settings
from django.test import TransactionTestCase, tag  # noqa
from django.test.utils import override_settings
from django_revision.apps import check_revision
from django_revision.revision import Revision, site_revision
from django_revision.views import RevisionMixin
from git import GitDB, Repo
from git.exc import InvalidGitRepositoryError

from ..models import TestModel


class TestRevision(TransactionTestCase):
    def setUp(self):
        path = settings.BASE_DIR
        repo = Repo(path, odbt=GitDB)
        self.tag = str(repo.git.describe(tags=True))
        try:
            self.branch = str(repo.active_branch)
            self.commit = str(repo.active_branch.commit)
        except TypeError:
            self.branch = "detached"
            self.commit = str(repo.commit())
        self.revision = f"{self.tag}:{self.branch}:{self.commit}"[0:75]

    @override_settings(REVISION=None)
    def test_no_git(self):
        path = mkdtemp()
        self.assertTrue(check_revision(working_dir=path).startswith("Revision invalid"))

    @override_settings(REVISION="1.1.1")
    def test_defaults_to_settings(self):
        path = mkdtemp()
        self.assertTrue(check_revision(working_dir=path).startswith("Revision: 1.1.1"))

    def test_revision_mixin(self):
        mixin = RevisionMixin()
        self.assertIn("revision", mixin.get_context_data())

    def test_model(self):
        test_model = TestModel()
        test_model.save()
        self.assertEqual(test_model.revision, self.revision)
        test_model = TestModel.objects.create()
        self.assertEqual(test_model.revision, self.revision)

    def test_revision(self):
        path = settings.BASE_DIR
        repo = Repo(path, odbt=GitDB)
        revision_tag = repo.git.describe(tags=True)
        self.assertEquals(revision_tag, site_revision.tag)

    def test_revision_branch(self):
        revision = Revision()
        self.assertEqual(revision.branch, self.branch)

    def test_revision_tag(self):
        revision = Revision()
        self.assertEqual(revision.tag, self.tag)

    def test_revision_commit(self):
        revision = Revision()
        self.assertEqual(revision.commit, self.commit)

    @override_settings(REVISION="0.0.0")
    def test_working_dir(self):
        folder = "/tmp"
        self.assertRaises(InvalidGitRepositoryError, Repo, folder, odbt=GitDB)
        self.assertEqual(Revision(working_dir=folder).revision, settings.REVISION)

    @skip("mock")
    @override_settings(REVISION="0.0.0")
    def test_manual_revision1(self):
        """Assert the django_revision does not set manually
        if repo can be found .
        """
        revision = Revision(manual_revision="0.0.0")
        self.assertNotEqual("0.0.0", revision.revision)

    def test_manual_revision2(self):
        """Assert the django_revision can be set manually
        and a working_dir is ignored.
        """
        revision = Revision(manual_revision="0.1.0", working_dir="/tmp")
        self.assertEqual(revision.revision, "0.1.0")
