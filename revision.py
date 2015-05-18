from git import Repo, GitDB, GitCommandError

from django.conf import settings


class Revision(object):

    def __init__(self):
        self._revision = None
        self.repo = Repo(self.source_folder, odbt=GitDB)
        try:
            self.tag = self.repo.git.describe(tags=True)
        except GitCommandError:  # if no tags, raises exception
            self.tag = ''
        self.branch = str(self.repo.active_branch)
        self.commit = str(self.repo.active_branch.commit)
        self.revision = '{0}:{1}'.format(self.branch, self.commit)

    def __repr__(self):
        return '{0}({1.tag!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.tag!s}'.format(self)

    @property
    def source_folder(self):
        if 'PROJECT_ROOT' not in dir(settings):
            raise AttributeError('Missing settings attribute: \'PROJECT_ROOT\' required by revision field class')
        return settings.PROJECT_ROOT

site_revision = Revision()
