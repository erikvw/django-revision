from tempfile import gettempdir, mkdtemp
from unittest.case import skip

from django.conf import settings
from django.test import TransactionTestCase
from django.test.utils import override_settings
from django.views.generic.base import ContextMixin
from git import GitCmdObjectDB, Repo
from git.exc import InvalidGitRepositoryError

from django_revision import Revision, check_revision, site_revision
from django_revision.revision import get_best_tag
from django_revision.views import RevisionMixin

from ..models import TestModel


class MyRevisionView(RevisionMixin, ContextMixin):
    pass


class TestRevision(TransactionTestCase):
    def setUp(self):
        path = settings.BASE_DIR
        repo = Repo(path, odbt=GitCmdObjectDB)
        self.tag = get_best_tag(repo)
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
        self.assertTrue(check_revision(path).startswith("Revision invalid"))

    @override_settings(REVISION="1.1.1")
    def test_defaults_to_settings(self):
        path = mkdtemp()
        revision_str = check_revision(path)  # .startswith("Revision: 1.1.1")
        self.assertIn("InvalidGitRepositoryError", revision_str)

    def test_revision_mixin(self):
        view = MyRevisionView()
        self.assertIn("revision", view.get_context_data())

    def test_model(self):
        test_model = TestModel()
        test_model.save()
        self.assertEqual(test_model.revision, self.revision)
        test_model = TestModel.objects.create()
        self.assertEqual(test_model.revision, self.revision)

    def test_revision(self):
        path = settings.BASE_DIR
        repo = Repo(path, odbt=GitCmdObjectDB)
        revision_tag = get_best_tag(repo)
        self.assertEqual(revision_tag, site_revision.tag)

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
        folder = gettempdir()
        self.assertRaises(InvalidGitRepositoryError, Repo, folder, odbt=GitCmdObjectDB)

    @override_settings(REVISION="0.0.0", DJANGO_REVISION_IGNORE_WORKING_DIR=True)
    def test_working_dir3(self):
        folder = gettempdir()
        self.assertEqual(Revision(working_dir=folder).revision, settings.REVISION)

    @skip("mock")
    @override_settings(REVISION="0.0.0")
    def test_manual_revision1(self):
        """Assert the django_revision does not set manually
        if repo can be found .
        """
        revision = Revision(manual_revision="0.0.0")
        self.assertNotEqual("0.0.0", revision.revision)

    @override_settings(REVISION=None, DJANGO_REVISION_IGNORE_WORKING_DIR=True)
    def test_manual_revision2(self):
        """Assert the django_revision can be set manually
        and a working_dir is ignored.
        """
        revision = Revision(manual_revision="0.1.0", working_dir=gettempdir())
        self.assertEqual(revision.revision, "0.1.0")
