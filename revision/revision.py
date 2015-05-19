from git import Repo, GitDB, GitCommandError, InvalidGitRepositoryError

from django.conf import settings


class Revision(object):

    def __init__(self, working_dir=None, manual_revision=None):
        try:
            manual_revision = settings.REVISION
        except AttributeError:
            pass
        if manual_revision:
            self.revision = manual_revision
            self.tag = ''
        else:
            try:
                self.working_dir = working_dir or settings.GIT_DIR
            except AttributeError:
                try:
                    self.working_dir = settings.BASE_DIR
                except AttributeError:
                    raise AttributeError(
                        'Missing settings attribute \'BASE_DIR\' or \'GIT_DIR\' '
                        'required by django-revision.')
            try:
                self.repo = Repo(self.working_dir, odbt=GitDB)
            except InvalidGitRepositoryError as e:
                raise InvalidGitRepositoryError(
                    'Invalid working folder. Got \'{}\'. The git \'working_dir\' '
                    'must the root of the git repo. Try setting GIT_DIR in settings.'.format(e))
            try:
                self.tag = self.repo.git.describe(tags=True)
            except GitCommandError:  # if no tags, raises exception
                self.tag = ''
            try:
                self.branch = str(self.repo.active_branch)
                self.commit = str(self.repo.active_branch.commit)
                self.revision = '{0}:{1}'.format(self.branch, self.commit)
            except TypeError:
                self.branch = 'detached'
                self.commit = str(self.repo.commit())
            self.revision = '{0}:{1}'.format(self.branch, self.commit)

    def __repr__(self):
        return '{0}({1.tag!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.tag!s}'.format(self)

site_revision = Revision()
