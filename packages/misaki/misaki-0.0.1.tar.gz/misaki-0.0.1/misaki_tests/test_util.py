import pytest
import sys

from misaki.util import (
    get_path,
    import_object,
    KeyPrefixMappingProxy,
    KeyPrefixMutableMappingProxy,
)


def test_import_object():
    assert import_object("sys.path", __name__) is sys.path


def test_get_path():
    d = {"a": {"b": {"c": 3}}}

    assert get_path(d, "a") is d["a"]
    assert get_path(d, "a.b") is d["a"]["b"]
    assert get_path(d, "a.x") is None
    assert get_path(d, "a.b.c") == 3
    assert get_path(d, "a.x", 7) == 7
    assert get_path(d, ["a", "b"]) == d["a"]["b"]


@pytest.mark.parametrize(
    "cls,mutable",
    [(KeyPrefixMappingProxy, False), (KeyPrefixMutableMappingProxy, True)],
)
def test_key_prefix_mapping(cls, mutable):
    d = {"a.b": 1, "b": 2, "a.c": 3, "a.": 4}

    m = cls(d, "a.")

    assert set(iter(m)) == set(("b", "c", ""))

    assert len(m) == 3

    assert m["b"] == 1
    assert m.get("") == 4
    assert m.get("notfound", 404) == 404

    with pytest.raises(KeyError):
        m["notfound"]

    if mutable:
        m["a"] = 5
        assert m["a"] == 5
        assert d["a.a"] == 5

        del m["b"]
        assert "b" not in m
        assert "a.b" not in d
    else:
        with pytest.raises(TypeError):
            m["a"] = 5
