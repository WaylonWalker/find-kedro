"""
punch versioning config, punch is used to change semver version of the project
in every necessary place and properly tag git commit with a release.

Install Punch

    $ pip install punch

To change version use punch -p <part> where part is major, minor, patch

    $ punch -p patch
"""
__config_version__ = 1

GLOBALS = {
    "serializer": "{{major}}.{{minor}}.{{patch}}",
}

FILES = ["setup.py", "find_kedro/__init__.py", "find_kedro/cli.py", "tests/test_cli.py"]

VERSION = ["major", "minor", "patch"]

VCS = {
    "name": "git",
    "commit_message": (
        "Version updated from {{ current_version }}" " to {{ new_version }}"
    ),
}
