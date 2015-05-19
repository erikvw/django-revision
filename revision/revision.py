from git import Repo, GitDB, GitCommandError, InvalidGitRepositoryError

from django.conf import settings


class Revision(object):

    def __init__(self, working_dir=None, manual_revision=None):
        self._manual_revision = manual_revision
        self._repo = None
        self._tag = None
        self._working_dir = working_dir
        self._revision = self.manual_revision

    @property
    def working_dir(self):
        """Returns the working_dir as either the Django BASE_DIR or
        a manually set GIT_DIR (if BASE_DIR is not the git repo)."""
        if self._working_dir is None:
            try:
                self._working_dir = settings.GIT_DIR
            except AttributeError:
                try:
                    self._working_dir = settings.BASE_DIR
                except AttributeError:
                    raise AttributeError(
                        'Missing settings attribute \'BASE_DIR\' or \'GIT_DIR\' '
                        'required by django-revision.')
        return self._working_dir

    @property
    def manual_revision(self):
        """Returns a manually set revision string, e.g set by the user in settings.REVISION."""
        if self._manual_revision is None:
            try:
                self._manual_revision = settings.REVISION
                self.revision = self._manual_revision
            except AttributeError:
                self._manual_revision = None
        return self._manual_revision

    @property
    def revision(self):
        """Returns a revision string of tag:branch:commit."""
        if not self._revision:
            self._revision = self.manual_revision
            if not self._revision:
                try:
                    self.branch = str(self.repo.active_branch)
                    self.commit = str(self.repo.active_branch.commit)
                    self.revision = '{0}:{1}'.format(self.branch, self.commit)
                except TypeError:
                    self.branch = 'detached'
                    self.commit = str(self.repo.commit())
                self._revision = '{}:{}:{}'.format(self.tag, self.branch, self.commit)
        return self._revision

    @property
    def tag(self):
        """Returns the tag from git describe."""
        if self._tag is None:
            try:
                self._tag = self.repo.git.describe(tags=True)
            except GitCommandError:
                self._tag = ''
        return self._tag

    @property
    def repo(self):
        """Returns a git repo object."""
        if not self._repo:
            try:
                self._repo = Repo(self.working_dir, odbt=GitDB)
            except InvalidGitRepositoryError as e:
                raise InvalidGitRepositoryError(
                    'Invalid git repo. Got \'{}\'. The git \'working_dir\' '
                    'must the root of the git repo. Try setting GIT_DIR in settings.'.format(e))
        return self._repo

    def __repr__(self):
        return '{0}({1.tag!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.tag!s}'.format(self)

site_revision = Revision()
