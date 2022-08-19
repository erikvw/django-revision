from typing import Optional

from django.conf import settings
from git import GitCmdObjectDB, GitCommandError, InvalidGitRepositoryError, Repo

from django_revision.constants import NO_TAG


class DummyBranch:
    commit = ""

    def __str__(self):
        return self.commit


def get_best_tag(repo):
    try:
        tag = repo.git.describe(tags=True)
    except GitCommandError:
        try:
            tag = str(repo.head.reference.commit)
        except TypeError as e:
            if "HEAD is a detached" not in str(e):
                raise
            tag = "detached"
    except (AttributeError, GitCommandError):
        try:
            tag = repo.tag
        except AttributeError:
            tag = settings.REVISION
    return tag


class DummyRepo:
    def __init__(self, tag=None):
        self.tag = tag
        self.branch = None
        self.active_branch = DummyBranch()
        self.commit = self.active_branch.commit or ""

    def __str__(self):
        return self.tag


class Revision:
    def __init__(
        self,
        working_dir: Optional[str] = None,
        manual_revision: Optional[str] = None,
        max_length: Optional[int] = None,
        ignore_invalid_working_dir: Optional[bool] = None,
    ):
        self._tag = None
        self.branch = None
        self.commit = None
        self.invalid = False
        self.max_length = max_length or 75
        self.ignore_invalid_working_dir = ignore_invalid_working_dir or getattr(
            settings, "DJANGO_REVISION_IGNORE_WORKING_DIR", False
        )
        self._working_dir = working_dir

        try:
            self.repo = Repo(self.working_dir, odbt=GitCmdObjectDB)
        except InvalidGitRepositoryError:
            if not self.ignore_invalid_working_dir:
                raise
            tag = manual_revision or getattr(settings, "REVISION", NO_TAG)
            self.repo = DummyRepo(tag=tag)
        try:
            self.branch = str(self.repo.active_branch)
            self.commit = str(self.repo.active_branch.commit)
        except TypeError:
            self.branch = "detached"
            self.commit = str(self.repo.commit())

        opts = ":".join([item for item in [self.tag, self.branch, self.commit] if item])
        self.revision = f"{opts}"[0 : self.max_length]
        if not self.revision:
            self.repo = DummyRepo(tag=f"no revision info! Check GIT_DIR={self.working_dir}.")
            self.invalid = True

    def __repr__(self):
        return f"{self.__class__.__name__}({self.working_dir}, {self.revision})"

    def __str__(self):
        return self.revision

    @property
    def tag(self):
        if not self._tag:
            self._tag = get_best_tag(self.repo)
        return self._tag

    @property
    def working_dir(self):
        if not self._working_dir:
            self._working_dir = getattr(settings, "GIT_DIR", None) or settings.BASE_DIR
            if not self._working_dir and not self.ignore_invalid_working_dir:
                raise InvalidGitRepositoryError(
                    "Invalid working directory. See settings.BASE_DIR"
                )

        return self._working_dir


site_revision = Revision()
