from collections.abc import Mapping, MutableMapping
import importlib

__all__ = ["import_object", "get_path"]

_BAD = []


class KeyPrefixMappingProxy(Mapping):
    def __init__(self, dictionary, prefix):
        self.dictionary = dictionary
        self.prefix = prefix

    def __getitem__(self, key):
        return self.dictionary[self.prefix + key]

    def __iter__(self):
        prefix = self.prefix
        n = len(prefix)
        for k in self.dictionary:
            if k.startswith(prefix):
                yield k[n:]

    def __len__(self):
        prefix = self.prefix
        return sum(k.startswith(prefix) for k in self.dictionary)


class KeyPrefixMutableMappingProxy(KeyPrefixMappingProxy, MutableMapping):
    def __setitem__(self, key, value):
        self.dictionary[self.prefix + key] = value

    def __delitem__(self, key):
        del self.dictionary[self.prefix + key]


def import_object(path, relative=None):
    """Use as ``import_object("os.stat", __name__)``. """

    module_name, _, member_name = path.rpartition(".")
    package = relative.rpartition(".")[0] if relative else None
    return getattr(importlib.import_module(module_name, package), member_name)


def get_path(mapping, keys, default=None):
    if isinstance(keys, str):
        keys = keys.split(".")

    for k in keys:
        v = mapping.get(k, _BAD)
        if v is _BAD:
            return default
        mapping = v

    return mapping
