class RevisionError(Exception):
    pass


class RevisionTomlError(Exception):
    pass


class RevisionGitError(Exception):
    pass


class RevisionGitDirDoesNotExist(Exception):
    pass


class RevisionPackageNotFoundError(Exception):
    pass
