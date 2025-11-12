import contextlib
import tomllib
import warnings
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from django.conf import settings
from django.core.management import color_style

style = color_style()


def ignore_working_dir() -> bool:
    return getattr(settings, "DJANGO_REVISION_IGNORE_WORKING_DIR", False)


def ignore_metadata() -> bool:
    return getattr(settings, "DJANGO_REVISION_IGNORE_METADATA", False)


def ignore_toml_file() -> bool:
    return getattr(settings, "DJANGO_REVISION_IGNORE_TOML_FILE", False)


def ignore_version_file() -> bool:
    return getattr(settings, "DJANGO_REVISION_IGNORE_VERSION_FILE", False)


def get_git_dir() -> Path | None:
    if path := getattr(settings, "GIT_DIR", settings.BASE_DIR):
        return Path(path)
    return None


def get_app_name() -> str | None:
    return getattr(settings, "APP_NAME", None)


def get_revision_from_metadata(app_name: str | None = None) -> str:
    revision = None
    if not ignore_metadata():
        app_name = app_name or get_app_name()
        try:
            revision = version(app_name)
        except PackageNotFoundError as e:
            warnings.warn(
                style.WARNING(f"Unable to determine revision from package metadata. Got {e}"),
                stacklevel=2,
            )
    return revision


def get_revision_from_toml_file(path: Path | None = None) -> str | None:
    revision = None
    if not ignore_toml_file():
        path = (path or Path(settings.BASE_DIR)) / "pyproject.toml"
        if path.exists():
            with path.open("rb") as f:
                toml_data = tomllib.load(f)
            with contextlib.suppress(KeyError):
                revision = toml_data["project"]["version"]
    return revision


def get_revision_from_version_file(path: Path | None = None) -> str | None:
    revision = None
    if not ignore_version_file():
        path = (path or Path(settings.BASE_DIR)) / "VERSION"
        if path.exists():
            with path.open("rb") as f:
                revision = f.read().decode("utf-8")
    return revision


def get_revision_from_settings() -> str:
    return getattr(settings, "REVISION", None) or getattr(
        settings, "DJANGO_REVISION_REVISION", None
    )
