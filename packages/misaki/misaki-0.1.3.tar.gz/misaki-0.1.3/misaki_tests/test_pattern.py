from misaki.pattern import Patterns

import yaml
import pkg_resources
import pytest


@pytest.fixture
def pattern_data():
    with pkg_resources.resource_stream(
        __name__, "test_pattern_data.yaml"
    ) as file:
        data = yaml.load(file)
    return data


def check_pattern_paths(pattern, paths):
    for pathspec in paths.split("\n"):
        if not pathspec:
            continue

        expected, path = pathspec.split(":", 1)
        expected = bool(int(expected))

        assert pattern.match(path) == expected


@pytest.mark.parametrize("key", ["py_simple", "py_expr", "py_expr_modify"])
def test_pattern_expr(pattern_data, key):
    pp = Patterns()
    pp.parse_definitions(pattern_data[key])

    check_pattern_paths(pp.patterns["python"], pattern_data["py_python_paths"])


def test_pattern_complex_expr(pattern_data):
    pp = Patterns()
    pp.parse_definitions(pattern_data["exclude"])

    check_pattern_paths(
        pp.patterns["relevant"], pattern_data["exclude_relevant_paths"]
    )
