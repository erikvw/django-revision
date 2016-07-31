from django.conf import settings

from git import Repo, GitDB, GitCommandError, InvalidGitRepositoryError


class Revision(object):

    def __init__(self, working_dir=None, manual_revision=None, max_length=None):
        self.revision = None
        self.max_length = max_length or 75
        self.working_dir = working_dir or settings.GIT_DIR
        try:
            self.revision = self.repo_revision or manual_revision or settings.REVISION
        except AttributeError:
            self.revision = 'no revision info!'

    @property
    def repo_revision(self):
        """Returns the revision as per the underlying repo or None."""
        revision = None
        try:
            repo = Repo(self.working_dir, odbt=GitDB)
            try:
                self.tag = repo.git.describe(tags=True)
            except GitCommandError:
                self.tag = ''
            try:
                self.branch = str(repo.active_branch)
                self.commit = str(repo.active_branch.commit)
            except TypeError:
                self.branch = 'detached'
                self.commit = str(repo.commit())
            revision = '{}:{}:{}'.format(self.tag, self.branch, self.commit)[0: self.max_length]
        except InvalidGitRepositoryError:
            pass
        return revision

    def __repr__(self):
        return '{0}({1.working_dir!r}, {1.manual_revision!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.django_revision!s}'.format(self)

site_revision = Revision()
