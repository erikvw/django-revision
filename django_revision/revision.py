from git import Repo, GitDB, GitCommandError, InvalidGitRepositoryError

from django.conf import settings


class Revision(object):

    def __init__(self, working_dir=None, manual_revision=None):
        self._manual_revision = manual_revision
        self._repo = None
        self._tag = None
        self._working_dir = working_dir
        self._revision = None
        self.max_length = 75

    def __repr__(self):
        return '{0}({1.working_dir!r}, {1.manual_revision!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.django_revision!s}'.format(self)

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

    @property
    def revision(self):
        """Returns a django_revision string of tag:branch:commit."""
        if not self._revision:
            self._revision = self.manual_revision
            if not self._revision:
                try:
                    self.branch = str(self.repo.active_branch)
                    self.commit = str(self.repo.active_branch.commit)
                    self._revision = '{0}:{1}'.format(self.branch, self.commit)
                except TypeError:
                    self.branch = 'detached'
                    self.commit = str(self.repo.commit())
                self._revision = '{}:{}:{}'.format(self.tag, self.branch, self.commit)
        return self._revision[0:self.max_length]

    @property
    def manual_revision(self):
        """Returns a manually set django_revision string, e.g set by the user in settings.REVISION."""
        if self._manual_revision is None:
            try:
                self._manual_revision = settings.REVISION
            except AttributeError:
                pass
        return self._manual_revision

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
                        'required by django_revision.')
        return self._working_dir

site_revision = Revision()
