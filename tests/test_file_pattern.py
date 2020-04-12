"""
tests pattern matching into various file patterns
"""
from pathlib import Path

import pytest

from find_kedro import find_kedro
from util import File, make_files_and_cd

content = [
    (
        2,
        ["nodes*"],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        2,
        "nodes*",
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        0,
        [1],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        0,
        [1.1],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        0,
        1,
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        0,
        1.1,
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        2,
        ["pipeline*"],
        [
            File(
                "nodes/pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        2,
        ["no_match", 1, 2, 1.1, "a", "pipeline*"],
        [
            File(
                "nodes/pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        2,
        ["*pipeline*"],
        [
            File(
                "nodes/de_pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        2,
        ["*"],
        [
            File(
                "nodes/de_pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        2,
        ["d?_pipeline*"],
        [
            File(
                "nodes/de_pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        2,
        ["de?pipeline.py"],
        [
            File(
                "nodes/de_pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        2,
        ["de_pipeline.py"],
        [
            File(
                "nodes/de_pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        0,
        ["pipeline"],
        [
            File(
                "nodes/de_pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        0,
        ["*nodes*"],
        [
            File(
                "nodes/de_pipeline.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        0,
        ["*nodes*"],
        [
            File(
                "nodes/nodes_module/de_pipeline.py",
                """\
                from kedro.pipeline import node
                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
]

contents = [("file", content)]


@pytest.mark.parametrize(" num_nodes, file_patterns, files", content)
def test_create_file(tmpdir, num_nodes, file_patterns, files):
    make_files_and_cd(tmpdir, files)

    print(f"testing scenario {file_patterns}")
    print(f'files created: {Path().glob("**/*")}')
    pipelines = find_kedro(directory=".", file_patterns=file_patterns, verbose=True)
    assert (
        len(pipelines["__default__"].nodes) == num_nodes
    ), f"did not collect all nodes from test using\npattern: {file_patterns}\nfiles: {[file.name for file in file_patterns]}"


@pytest.mark.parametrize(" num_nodes, file_patterns, files", content)
def test_create_file_full_path(tmpdir, num_nodes, file_patterns, files):
    make_files_and_cd(tmpdir, files)

    print(f"testing scenario {file_patterns}")
    print(f'files created: {Path().glob("**/*")}')
    pipelines = find_kedro(directory=tmpdir, file_patterns=file_patterns, verbose=True)
    assert (
        len(pipelines["__default__"].nodes) == num_nodes
    ), f"did not collect all nodes from test using\npattern: {file_patterns}\nfiles: {[file.name for file in file_patterns]}"
