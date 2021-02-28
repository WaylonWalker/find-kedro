"""
tests cli functionality.

Ensure other tests function properly through the cli as well by reusing their content
"""
import pytest
from click.testing import CliRunner
from more_itertools import roundrobin

from find_kedro.cli import cli
from test_discover_py import content as discover_content
from test_file_pattern import content as file_pattern_content
from test_pattern import content as pattern_content
from util import make_files_and_cd

__version__ = "0.1.1"


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_version_verbose():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version", "--verbose"])
    assert result.exit_code == 0
    assert __version__ in result.output


@pytest.mark.parametrize(" num_nodes, patterns, files", pattern_content)
def test_pattern(tmpdir, num_nodes, patterns, files):
    make_files_and_cd(tmpdir, files)
    runner = CliRunner()
    if type(patterns) == list:
        args = list(roundrobin(["--patterns"] * len(patterns), patterns))
        result = runner.invoke(cli, args)
    else:
        result = runner.invoke(cli, ["--patterns", patterns])
    import json

    pipeline = json.loads(result.output)

    assert result.exit_code == 0
    assert len(pipeline["__default__"]) == num_nodes


@pytest.mark.parametrize(" num_nodes, patterns, files", pattern_content)
def test_pattern_verbose(tmpdir, num_nodes, patterns, files):
    make_files_and_cd(tmpdir, files)
    runner = CliRunner()
    result = runner.invoke(cli, ["--verbose",])
    assert result.exit_code == 0


@pytest.mark.parametrize(" num_nodes, file_patterns, files", file_pattern_content)
def test_file_pattern(tmpdir, num_nodes, file_patterns, files):
    make_files_and_cd(tmpdir, files)

    runner = CliRunner()
    if type(file_patterns) == list:
        args = list(roundrobin(["--file-patterns"] * len(file_patterns), file_patterns))
        result = runner.invoke(cli, args)
    else:
        result = runner.invoke(cli, ["--file-patterns", file_patterns])
    import json

    pipelines = json.loads(result.output)

    assert result.exit_code == 0
    assert (
        len(pipelines["__default__"]) == num_nodes
    ), f"did not collect all nodes from test using\npattern: {file_patterns}\nfiles: {[file.name for file in file_patterns]}"


@pytest.mark.parametrize("name, num_nodes, files", discover_content)
def test_file_patterns(tmpdir, name, num_nodes, files):
    make_files_and_cd(tmpdir, files)
    runner = CliRunner()
    # if type(patterns) == list:
    # args = list(roundrobin(['--file-patterns'] * len(patterns), patterns))
    # result = runner.invoke(cli, args)
    # else:
    # result = runner.invoke(cli, ['--patterns', patterns])
    result = runner.invoke(cli)
    import json

    pipeline = json.loads(result.output)

    assert result.exit_code == 0
    assert len(pipeline["__default__"]) == num_nodes


# def test_main()
