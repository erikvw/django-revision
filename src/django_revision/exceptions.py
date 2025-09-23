class RevisionError(Exception):
    pass


class RevisionTomlError(Exception):
    pass


class RevisionGitError(Exception):
    pass


class RevisionGitDirDoesNotExist(Exception):  # noqa: N818
    pass


class RevisionPackageNotFoundError(Exception):
    pass
