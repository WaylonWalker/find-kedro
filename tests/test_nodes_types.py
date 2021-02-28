"""
This module tests the creation of pipeline nodes from various different types
and combinations of types.
"""
import textwrap

import pytest

from find_kedro import find_kedro

contents = [
    (
        "single_nodes",
        2,
        """\
    from kedro.pipeline import node

    node_a_b = node(lambda x: x, "a", "b", name="a_b")
    node_b_c = node(lambda x: x, "b", "c", name="b_c")
    """,
    ),
    (
        "list_nodes",
        2,
        """\
    from kedro.pipeline import node

    nodes = [
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c")
        ]
    """,
    ),
    (
        "set_nodes",
        2,
        """\
    from kedro.pipeline import node

    nodes = {
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c")
        }
    """,
    ),
    (
        "tuple_nodes",
        2,
        """\
    from kedro.pipeline import node

    nodes = (
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c")
        )
    """,
    ),
    (
        "pipeline_nodes",
        2,
        """\
    from kedro.pipeline import node, Pipeline

    nodes = Pipeline([
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c")
        ])
    """,
    ),
    (
        "pipeline_list_nodes",
        4,
        """\
    from kedro.pipeline import node, Pipeline

    nodes_pipeline = Pipeline([
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c"),
        ])
    nodes_list = [
        node(lambda x: x, "a2", "b2", name="a_b2"),
        node(lambda x: x, "b2", "c2", name="b_c2"),
        ]
    """,
    ),
    (
        "pipeline_nodes_nodes",
        4,
        """\
    from kedro.pipeline import node, Pipeline

    nodes_pipeline = Pipeline([
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c"),
        ])
    node_a2 = node(lambda x: x, "a2", "b2", name="a_b2")
    node_b2 = node(lambda x: x, "b2", "c2", name="b_c2")
    """,
    ),
    (
        "list_nodes_nodes",
        4,
        """\
    from kedro.pipeline import node

    nodes_pipeline = [
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c"),
        ]
    node_a2 = node(lambda x: x, "a2", "b2", name="a_b2")
    node_b2 = node(lambda x: x, "b2", "c2", name="b_c2")
    """,
    ),
    (
        "dynamic_list_nodes",
        100,
        """\
    from kedro.pipeline import node

    nodes_pipeline = [ node(lambda x: x, f"a{n}", f"a{n+1}", name=f"a{n}_a{n+1}") for n in range(100)]
    """,
    ),
    (
        "dynamic_pipeline_nodes",
        100,
        """\
    from kedro.pipeline import node, Pipeline

    nodes_pipeline = Pipeline([ node(lambda x: x, f"a{n}", f"a{n+1}", name=f"a{n}_a{n+1}") for n in range(100)])
    """,
    ),
    (
        "nested_list_nodes",
        4,
        """\
    from kedro.pipeline import node

    nodes_pipeline = [
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c"),
        [
            node(lambda x: x, "a2", "b2", name="a_b2"),
            node(lambda x: x, "b2", "c2", name="b_c2"),
        ]
        ]
    """,
    ),
    (
        "nested_tuple_nodes",
        4,
        """\
    from kedro.pipeline import node

    nodes_pipeline = (
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c"),
        (
            node(lambda x: x, "a2", "b2", name="a_b2"),
            node(lambda x: x, "b2", "c2", name="b_c2"),
        )
        )
    """,
    ),
    (
        "nested_set_nodes",
        4,
        """\
    from kedro.pipeline import node

    nodes_pipeline = {
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c"),
        (
            node(lambda x: x, "a2", "b2", name="a_b2"),
            node(lambda x: x, "b2", "c2", name="b_c2"),
        )
        }
    """,
    ),
    (
        "function_nodes",
        2,
        """\
    from kedro.pipeline import Pipeline, node

    def create_pipeline():
        return Pipeline([
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c"),
        ]
        )
    """,
    ),
    (
        "function_single_nodes",
        4,
        """\
    from kedro.pipeline import Pipeline, node

    node_a_b = node(lambda x: x, "a", "b", name="a_b")
    node_b_c = node(lambda x: x, "b", "c", name="b_c")

    def create_pipeline():
        return Pipeline([
        node(lambda x: x, "fa", "fb", name="fa_fb"),
        node(lambda x: x, "fb", "fc", name="fb_fc"),
        ]
        )
    """,
    ),
    (
        "function_list_nodes",
        4,
        """\
    from kedro.pipeline import Pipeline, node

    nodes = [
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c")
    ]

    def create_pipeline():
        return Pipeline([
        node(lambda x: x, "fa", "fb", name="fa_fb"),
        node(lambda x: x, "fb", "fc", name="fb_fc"),
        ]
        )
    """,
    ),
    (
        "list_create_pipeline",
        2,
        """\
    from kedro.pipeline import Pipeline, node

    creaste_pipeline = [
        node(lambda x: x, "a", "b", name="a_b"),
        node(lambda x: x, "b", "c", name="b_c")
    ]
    """,
    ),
]


@pytest.mark.parametrize("name, num_nodes, content", contents)
def test_create_file(tmpdir, name, num_nodes, content):
    p = tmpdir.mkdir("nodes").join(f"{ name }.py")
    p.write(textwrap.dedent(content))
    pipelines = find_kedro(directory=tmpdir, verbose=True)
    assert list(pipelines.keys()) == [f"nodes.{ name }", "__default__"]
    assert (
        len(pipelines["__default__"].nodes) == num_nodes
    ), f"did not collect all nodes from { name }.py"
    assert len(tmpdir.listdir()) == 1
