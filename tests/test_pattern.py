"""
tests various pattern matching for node/pipeline variables.

"""
from pathlib import Path

import pytest

from find_kedro import find_kedro
from util import File, make_files_and_cd

content = [
    (
        2,
        ["node*"],
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
        ["dont_match", 1, 1.1, 0.123, "node*"],
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
        ["node_?_?"],
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
        1,
        ["node_a_?"],
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
        [""],
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
        ["*node*"],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")

                node_lambda = lambda x: x
                node_list = list()
                node_tuple = tuple()
                node_dict = dict()
                node_set = set()
                """,
            )
        ],
    ),
    (
        0,
        ["*node*"],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_lambda = lambda x: x
                node_list = list()
                node_tuple = tuple()
                node_dict = dict()
                node_set = set()
                """,
            )
        ],
    ),
    (
        2,
        "node*",
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
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                pipeline_one = [
                    node(lambda x: x, "a", "b", name="a_b"),
                    node(lambda x: x, "b", "c", name="b_c"),
                    ]
                """,
            )
        ],
    ),
    (
        0,
        ["pipeline"],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                pipeline_one = [
                    node(lambda x: x, "a", "b", name="a_b"),
                    node(lambda x: x, "b", "c", name="b_c"),
                    ]
                """,
            )
        ],
    ),
    (
        2,
        ["pipeline_one"],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                pipeline_one = [
                    node(lambda x: x, "a", "b", name="a_b"),
                    node(lambda x: x, "b", "c", name="b_c"),
                    ]
                pipeline_two= [
                    node(lambda x: x, "a2", "b2", name="a2_b2"),
                    node(lambda x: x, "b2", "c2", name="b2_c2"),
                    ]
                """,
            )
        ],
    ),
    (
        4,
        ["pipeline*"],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                pipeline_one = [
                    node(lambda x: x, "a", "b", name="a_b"),
                    node(lambda x: x, "b", "c", name="b_c"),
                    ]
                pipeline_two= [
                    node(lambda x: x, "a2", "b2", name="a2_b2"),
                    node(lambda x: x, "b2", "c2", name="b2_c2"),
                    ]
                """,
            )
        ],
    ),
    (
        4,
        ["pipeline_?"],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                pipeline_a = [
                    node(lambda x: x, "a", "b", name="a_b"),
                    node(lambda x: x, "b", "c", name="b_c"),
                    ]
                pipeline_b = [
                    node(lambda x: x, "a2", "b2", name="a2_b2"),
                    node(lambda x: x, "b2", "c2", name="b2_c2"),
                    ]
                """,
            )
        ],
    ),
    (
        4,
        ["pipeline_a", "pipeline_b"],
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                pipeline_a = [
                    node(lambda x: x, "a", "b", name="a_b"),
                    node(lambda x: x, "b", "c", name="b_c"),
                    ]
                pipeline_b = [
                    node(lambda x: x, "a2", "b2", name="a2_b2"),
                    node(lambda x: x, "b2", "c2", name="b2_c2"),
                    ]
                """,
            )
        ],
    ),
]

contents = [("file", content)]


@pytest.mark.parametrize(" num_nodes, patterns, files", content)
def test_create_file(tmpdir, num_nodes, patterns, files):
    "test find-kedro works with various patterns for pipeline variables"
    make_files_and_cd(tmpdir, files)

    print(f"testing scenario {patterns}")
    print(f'files created: {list(Path().glob("**/*"))}')
    pipelines = find_kedro(directory=".", patterns=patterns, verbose=True)
    assert (
        len(pipelines["__default__"].nodes) == num_nodes
    ), f"did not collect all nodes from test using\npattern: {patterns}\nfiles: {[file.name for file  in files]}"
