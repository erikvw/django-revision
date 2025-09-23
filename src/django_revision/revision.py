from __future__ import annotations

import warnings
from pathlib import Path

from django.conf import settings
from django.core.management import color_style
from git import GitCmdObjectDB, GitCommandError, InvalidGitRepositoryError, Repo

from .exceptions import RevisionError, RevisionGitDirDoesNotExist, RevisionGitError
from .utils import (
    get_app_name,
    get_git_dir,
    get_revision_from_metadata,
    get_revision_from_settings,
    get_revision_from_toml_file,
    get_revision_from_version_file,
    ignore_working_dir,
)

style = color_style()


class Revision:
    def __init__(
        self,
        max_length: str | int | None = None,
        app_name: str | None = None,
        toml_path: Path | str | None = None,
        verbose: bool | None = None,
    ):
        self._revision = None
        self._tag = None
        self._repo = None
        self._branch = None
        self._commit = None
        self._settings_revision = None
        self.max_length = max_length or 75
        self.app_name = app_name or get_app_name()
        self.toml_path = Path(toml_path) if toml_path else Path(settings.BASE_DIR)
        self.verbose = verbose

    def __repr__(self):
        return f"{self.__class__.__name__}({self.revision})"

    def __str__(self):
        return self.revision

    @property
    def revision(self) -> str:
        """Returns a revision number.

        Initially assumes the BASE_DIR is a git repo and looks for
        the most recent tag or raises.

        if DJANGO_REVISION_IGNORE_WORKING_DIR=True:
            1. looks for metadata version
            2. checks settings.REVISION
            3. checks pyproject.toml
        """

        if not self._revision:
            if not ignore_working_dir():
                self._revision = self.get_revision_from_git_tag()
                if self.verbose:
                    warnings.warn(
                        style.WARNING("Getting revision number from git"), stacklevel=2
                    )
            elif revision := get_revision_from_metadata():
                self._revision = revision
                if self.verbose:
                    warnings.warn(
                        style.WARNING("Getting revision number from package metata"),
                        stacklevel=2,
                    )
            elif revision := get_revision_from_toml_file(self.toml_path):
                self._revision = revision
                if self.verbose:
                    warnings.warn(
                        style.WARNING("Getting revision number from pyproject.toml"),
                        stacklevel=2,
                    )
            elif revision := get_revision_from_version_file(Path(settings.BASE_DIR)):
                self._revision = revision
                if self.verbose:
                    warnings.warn(
                        style.WARNING("Getting revision number from VERSION file"),
                        stacklevel=2,
                    )
            elif revision := get_revision_from_settings():
                self._revision = revision
                warnings.warn(
                    style.ERROR(
                        "Getting revision number from settings.REVISION (not recommended)."
                    ),
                    stacklevel=2,
                )
            else:
                raise RevisionError(
                    "Unable to determine the revision number. "
                    f"1. `settings.DJANGO_REVISION_IGNORE_WORKING_DIR="
                    f"{ignore_working_dir()}` so this is not a git repository. "
                    f"2. Got None from metadata for APP_NAME={get_app_name()}. "
                    "3. Looked for [project][version] in `pyproject.toml` file but "
                    "file not found in {settings.BASE_DIR}. "
                    "4. settings.REVISION has not been set. "
                )
        return self._revision

    def get_revision(self) -> str:
        return self.revision

    def get_revision_from_git_tag(self) -> str:
        opts = ":".join([item for item in [self.tag, self.branch, self.commit] if item])
        return f"{opts}"[0 : self.max_length]

    @property
    def repo(self):
        if not self._repo:
            if not get_git_dir().exists():
                raise RevisionGitDirDoesNotExist(
                    "Unable to determine the revision number. "
                    f"Invalid GIT_DIR or BASE_DIR. Got {get_git_dir()}."
                )
            try:
                self._repo = Repo(str(get_git_dir()), odbt=GitCmdObjectDB)
            except InvalidGitRepositoryError as e:
                raise RevisionGitError(
                    "Unable to determine the revision number. settings.GIT_DIR is "
                    "not a git repository. Check the folder or set "
                    "`settings.DJANGO_REVISION_IGNORE_WORKING_DIR=True. "
                    f"Got `settings.GIT_DIR={get_git_dir()}`"
                ) from e
        return self._repo

    @property
    def branch(self):
        if not self._branch:
            try:
                self._branch = str(self.repo.active_branch)
            except TypeError:
                self._branch = "detached"
        return self._branch

    @property
    def commit(self):
        if not self._commit:
            try:
                self._commit = str(self.repo.active_branch.commit)
            except TypeError:
                self._commit = str(self.repo.commit())
        return self._commit

    @property
    def tag(self) -> str:
        if not self._tag:
            try:
                self._tag = self.repo.git.describe(tags=True)
            except GitCommandError:
                try:
                    self._tag = str(self.repo.head.reference.commit)
                except TypeError as e:
                    if "HEAD is a detached" not in str(e):
                        raise RevisionError(e) from e
                    self._tag = "detached"
            except AttributeError:
                try:
                    self._tag = self.repo.tag
                except AttributeError:
                    self._tag = ""
        return self._tag


if getattr(settings, "DJANGO_REVISION_AUTODISCOVER", True):
    site_revision = Revision()
