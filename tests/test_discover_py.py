"""
tests various different patterns of library and ensures that the default patterns
will find the nodes.  This ensures that the project structure does not matter.
"""
import pytest

from find_kedro import find_kedro
from util import File, make_files_and_cd

content = [
    (
        "onefile",
        2,
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
        "deeply nested file",
        2,
        [
            File(
                "nodes/that/are/deeply/nested/without/any/init/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            )
        ],
    ),
    (
        "two separate files",
        4,
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            ),
            File(
                "nodes/nodes2.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a2", "b2", name="a2_b2")
                node_b_c = node(lambda x: x, "b2", "c2", name="b2_c2")
                """,
            ),
        ],
    ),
    (
        "two files, one match, one no match",
        2,
        [
            File(
                "nodes/nodes.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a", "b", name="a_b")
                node_b_c = node(lambda x: x, "b", "c", name="b_c")
                """,
            ),
            File(
                "nodes/no_match.py",
                """\
                from kedro.pipeline import node

                node_a_b = node(lambda x: x, "a2", "b2", name="a2_b2")
                node_b_c = node(lambda x: x, "b2", "c2", name="b2_c2")
                """,
            ),
        ],
    ),
    (
        "two files, project/[nodes, functions]",
        2,
        [
            File(
                "project/nodes.py",
                """\
                from kedro.pipeline import node
                from .functions import example_function

                node_a_b = node(example_function, "a", "b", name="a_b")
                node_b_c = node(example_function, "b", "c", name="b_c")
                """,
            ),
            File(
                "project/functions.py",
                """\
                def example_function(data):
                    pass
                """,
            ),
        ],
    ),
    (
        "two files, project/de/[nodes, functions]",
        2,
        [
            File(
                "project/de/nodes.py",
                """\
                from kedro.pipeline import node
                from .functions import example_function

                node_a_b = node(example_function, "a", "b", name="a_b")
                node_b_c = node(example_function, "b", "c", name="b_c")
                """,
            ),
            File(
                "project/de/functions.py",
                """\
                def example_function(data):
                    pass
                """,
            ),
        ],
    ),
    (
        "two files, project/de/nodes project/ds/nodes",
        2,
        [
            File(
                "project/de/nodes.py",
                """\
                from kedro.pipeline import node
                from ..ds.functions import example_function

                nodes_a_b = node(example_function, "a", "b", name="a_b")
                nodes_b_c = node(example_function, "b", "c", name="b_c")

                example_function('a')
                """,
            ),
            File(
                "project/ds/functions.py",
                """\
                def example_function(data):
                    pass
                """,
            ),
            File(
                "project/__init__.py",
                """\
                # from . import de
                # from . import ds
                """,
            ),
        ],
    ),
]

contents = [("file", content)]


@pytest.mark.parametrize("name, num_nodes, files", content)
def test_create_file(tmpdir, name, num_nodes, files):
    "test find-kedro can find and assemble pipeines in various ways"
    make_files_and_cd(tmpdir, files)

    print(f"testing scenario {name}")
    pipelines = find_kedro(directory=".", verbose=True)
    assert (
        len(pipelines["__default__"].nodes) == num_nodes
    ), f"did not collect all nodes from { name }.py"
