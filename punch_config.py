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
