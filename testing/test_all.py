from sourcedeps import parse_source
import os
import pytest
import logging


logging.basicConfig(level=logging.DEBUG)


@pytest.mark.parametrize(
    "filename,nodes,edges",
    [
        ("basic.py", {"foo", "bar"}, {("foo", "bar")}),
        ("diverging.py", {"foo", "bar", "baz"}, {("foo", "bar"), ("foo", "baz")}),
        ("multi_level.py", {"foo", "bar", "baz"}, {("foo", "bar"), ("bar", "baz")}),
        (
            "other_statements.py",
            {"foo", "bar", "baz"},
            {("foo", "bar"), ("bar", "baz")},
        ),
        ("assignment.py", {"foo", "bar"}, {("bar", "foo")}),
        (
            "classdef.py",
            {"f.something", "Foo", "bar"},
            {("bar", "f.something"), ("bar", "Foo")},
        ),
    ],
)
def test_example_file(filename, nodes, edges):
    graph = parse_source(os.path.join("testing", "examples", filename))

    assert set(graph.nodes()) == nodes
    assert set(graph.edges()) == edges


def test_parsing_source_itself_does_not_error():
    graph = parse_source(os.path.join("sourcedeps", "__init__.py"))

    # No exception means no errors were found
