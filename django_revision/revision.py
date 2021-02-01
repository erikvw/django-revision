from pathlib import PurePath

from django.conf import settings
from git import GitCommandError, GitDB, InvalidGitRepositoryError, Repo


class DummyBranch:
    commit = ""

    def __str__(self):
        return self.commit


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
        working_dir=None,
        manual_revision=None,
        max_length=None,
    ):
        self._tag = None
        self.branch = None
        self.commit = None
        self.invalid = False
        self.max_length = max_length or 75

        try:
            self.working_dir = working_dir or settings.GIT_DIR
        except AttributeError:
            self.working_dir = str(PurePath(settings.BASE_DIR).parent)
        try:
            self.repo = Repo(self.working_dir, odbt=GitDB)
        except InvalidGitRepositoryError:
            try:
                self.repo = DummyRepo(tag=settings.REVISION)
            except AttributeError:
                self.repo = DummyRepo(tag=manual_revision)
        try:
            self.branch = str(self.repo.active_branch)
            self.commit = str(self.repo.active_branch.commit)
        except TypeError:
            self.branch = "detached"
            self.commit = str(self.repo.commit())

        opts = ":".join([item for item in [self.tag, self.branch, self.commit] if item])
        self.revision = f"{opts}"[0 : self.max_length]
        if not self.revision:
            self.repo = DummyRepo(
                tag=f"no revision info! Check GIT_DIR={self.working_dir}."
            )
            self.invalid = True

    def __repr__(self):
        return f"{self.__class__.__name__}({self.working_dir}, {self.revision})"

    def __str__(self):
        return f"{self.revision}"

    @property
    def tag(self):
        if not self._tag:
            try:
                self._tag = self.repo.git.describe(tags=True)
            except GitCommandError:
                self._tag = str(self.repo.head.reference.commit)
            except AttributeError:
                self._tag = self.repo.tag
        return self._tag


site_revision = Revision()
