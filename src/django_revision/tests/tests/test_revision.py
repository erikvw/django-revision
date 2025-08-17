import os
import tempfile
from pathlib import Path
from tempfile import gettempdir
from unittest.mock import patch

import git
from django.conf import settings
from django.test import TransactionTestCase
from django.test.utils import override_settings, tag
from django.views.generic.base import ContextMixin

from django_revision import Revision
from django_revision.exceptions import RevisionError, RevisionGitError
from django_revision.views import RevisionMixin

from ..models import TestModel


class MyRevisionView(RevisionMixin, ContextMixin):
    pass


def create_temp_repo_with_tag():
    repo = create_temp_repo_without_tag()
    repo.create_tag("0.0.1")
    file_path = os.path.join(repo.working_dir, "test_file2.txt")
    with open(file_path, "w") as f:
        f.write("This is another test file.")
    repo.index.add(["test_file2.txt"])
    repo.index.commit("add test_file2.txt")
    repo.create_tag("0.0.2")
    return repo


def create_temp_repo_without_tag():
    repo_path = tempfile.mkdtemp()
    repo = git.Repo.init(repo_path)
    file_path = os.path.join(repo_path, "test_file.txt")
    with open(file_path, "w") as f:
        f.write("This is a test file.")
    repo.index.add(["test_file.txt"])
    repo.index.commit("Initial commit for testing")
    return repo


class TestRevision(TransactionTestCase):

    @override_settings(REVISION=None, GIT_DIR=create_temp_repo_with_tag().working_dir)
    def test_is_a_git_dir_with_tag(self):
        revision = Revision()
        self.assertTrue(str(revision).startswith("0.0.2"))
        self.assertTrue("master" in str(revision))

    @override_settings(
        REVISION=None, GIT_DIR=create_temp_repo_without_tag().working_dir
    )
    def test_is_a_git_dir_without_tag(self):
        revision = Revision()
        self.assertFalse(str(revision).startswith("0.0"))
        self.assertTrue("master" in str(revision))

    @override_settings(REVISION=None, GIT_DIR=gettempdir())
    def test_not_a_git_dir(self):
        revision = Revision()
        self.assertRaises(RevisionGitError, revision.get_revision)

    @override_settings(
        REVISION="0.0.1",
        DJANGO_REVISION_IGNORE_WORKING_DIR=True,
        DJANGO_REVISION_IGNORE_TOML_FILE=True,
        BASE_DIR=gettempdir(),
        DJANGO_REVISION_AUTODISCOVER=False,
    )
    def test_defaults_to_metadata(self):
        self.assertRegex(str(Revision()), "^[0-9]{1}\\.[0-9]{1}\\.[0-9]{1}$")
        self.assertNotEqual(str(Revision()), "0.0.1")

    @override_settings(
        REVISION="0.0.1",
        DJANGO_REVISION_IGNORE_WORKING_DIR=True,
        DJANGO_REVISION_IGNORE_METADATA=True,
        BASE_DIR=gettempdir(),
        DJANGO_REVISION_AUTODISCOVER=False,
    )
    def test_defaults_to_toml(self):
        toml_content = """
        [project]
        version = "9.9.9"
        """
        with open(Path(settings.BASE_DIR) / "pyproject.toml", "w") as f:
            f.write(toml_content)
        self.assertEqual(str(Revision()), "9.9.9")

    @override_settings(
        REVISION="0.0.1",
        DJANGO_REVISION_IGNORE_WORKING_DIR=True,
        DJANGO_REVISION_IGNORE_METADATA=True,
        DJANGO_REVISION_IGNORE_TOML_FILE=True,
        BASE_DIR=gettempdir(),
        DJANGO_REVISION_AUTODISCOVER=False,
    )
    def test_defaults_to_version_file(self):
        content = "8.8.8"
        with open(Path(settings.BASE_DIR) / "VERSION", "w") as f:
            f.write(content)
        self.assertEqual(str(Revision()), "8.8.8")

    @patch("django_revision.revision.get_revision_from_metadata")
    @override_settings(
        REVISION="1.1.1",
        DJANGO_REVISION_IGNORE_WORKING_DIR=True,
        DJANGO_REVISION_IGNORE_METADATA=True,
        DJANGO_REVISION_IGNORE_TOML_FILE=True,
        DJANGO_REVISION_IGNORE_VERSION_FILE=True,
        BASE_DIR=gettempdir(),
    )
    def test_defaults_to_settings(self, mock_get_revision_from_metadata):
        mock_get_revision_from_metadata.return_value = None
        self.assertIn("1.1.1", str(Revision()))

    @override_settings(REVISION=None, GIT_DIR=create_temp_repo_with_tag().working_dir)
    def test_revision_mixin(self):
        view = MyRevisionView()
        self.assertIn("revision", view.get_context_data())
        self.assertIn("0.0.2", str(view.get_context_data()))

    @override_settings(REVISION=None, GIT_DIR=create_temp_repo_with_tag().working_dir)
    def test_model(self):
        test_model = TestModel()
        test_model.save()
        self.assertRegex(str(Revision())[:5], "^[0-9]{1}\\.[0-9]{1}\\.[0-9]{1}$")
        self.assertEqual(test_model.revision, str(Revision()))
        test_model = TestModel.objects.create()
        self.assertEqual(test_model.revision, str(Revision()))

    @override_settings(REVISION=None, GIT_DIR=create_temp_repo_with_tag().working_dir)
    def test_revision_branch(self):
        revision = Revision()
        self.assertEqual("master", revision.branch)
        self.assertIn("master", str(Revision()))

    @override_settings(REVISION=None, GIT_DIR=create_temp_repo_with_tag().working_dir)
    def test_revision_tag(self):
        revision = Revision()
        self.assertEqual("0.0.2", revision.tag)
        self.assertIn("0.0.2", str(Revision()))

    @override_settings(REVISION=None, GIT_DIR=create_temp_repo_with_tag().working_dir)
    def test_revision_commit(self):
        revision = Revision()
        self.assertIsNotNone(revision.commit)
        self.assertIn(revision.commit, str(Revision()))

    @tag("6")
    @override_settings(
        REVISION=None,
        BASE_DIR=gettempdir(),
        DJANGO_REVISION_IGNORE_WORKING_DIR=True,
        DJANGO_REVISION_IGNORE_METADATA=True,
        DJANGO_REVISION_IGNORE_TOML_FILE=True,
        DJANGO_REVISION_IGNORE_VERSION_FILE=True,
        DJANGO_REVISION_AUTODISCOVER=False,
    )
    def test_revision_fails(self):
        self.assertRaises(RevisionError, Revision().get_revision)
