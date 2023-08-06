import re
from pathlib import PurePosixPath
from typing import Union


class PatternParseError(ValueError):
    pass


def _parse_single_item_dict(dictionary: dict):
    if not isinstance(dictionary, dict):
        raise PatternParseError("{!r} must be a dictionary".format(dictionary))

    if len(dictionary.keys()) != 1:
        raise PatternParseError(
            "dictionary {!r} must have exactly 1 key".format(dictionary)
        )

    item, = dictionary.items()

    return item


class Patterns:
    _pattern_re = re.compile(
        r"^(?P<negate>!?)(?:"
        r"(?P<label>[^!:]+)|"
        r"(?:(?P<pattern_type>[^!:]+):(?P<pattern_value>.+))"
        r")$"
    )

    def __init__(self):
        self.patterns = {}

    def parse_operator_and(self, key, value):
        return AndPattern(value)

    def parse_operator_or(self, key, value):
        return OrPattern(value)

    def parse_operator_not(self, key, value):
        return NotPattern(value)

    def parse_node(self, node):
        if isinstance(node, dict):
            key, value = _parse_single_item_dict(node)

            method = getattr(self, "parse_operator_" + key, None)

            if method is None:
                raise PatternParseError("unknown operator {!r}".format(node))

            return method(key, [self.parse_node(x) for x in value])

        elif isinstance(node, str):
            m = self._pattern_re.match(node)
            if m is None:
                raise PatternParseError("parsing {!r}".format(node))

            d = m.groupdict()

            if d["label"] is not None:
                pat = self.patterns[d["label"]]
            else:
                pattern_type = d["pattern_type"]
                pattern_value = d["pattern_value"]
                if pattern_type == "re":
                    pat = RegexPattern(pattern_value)
                else:
                    raise PatternParseError(
                        "unknown pattern type {!r} for {!r}".format(
                            pattern_type, node
                        )
                    )

            if bool(d["negate"]):
                pat = NotPattern([pat])

            return pat

    def parse_definitions(self, definitions):
        d = self.patterns
        if not isinstance(definitions, list):
            raise PatternParseError(
                "pattern definitions {!r} must be a list", format(definitions)
            )
        for definition in definitions:
            name, node = _parse_single_item_dict(definition)
            d[name] = self.parse_node(node)

    def evaluate_patterns(self, path: str, keys=None):
        """Evaluate each of the patterns listed in ``keys`` (or all of
them if None) against ``path``, and return the result as a dictionary
where keys are pattern labels and values are whether the pattern
matched on that path."""

        patterns = self.patterns

        if keys is None:
            keys = patterns.keys()

        result = {}
        context = None

        for k in keys:
            pattern = patterns[k]

            if context is None:
                context = pattern.path_to_context(path)

            result[k] = pattern._match(context)

        return result


class BasePattern:
    def path_to_context(self, path: Union[str, PurePosixPath]) -> str:
        path = "/" + str(path).lstrip("/")
        return dict(path=path, cache={})

    def match(self, path: str) -> bool:
        return self._match(self.path_to_context(path))

    def _match_uncached(self, context: dict) -> bool:
        """Match ``context["path"]`` against this pattern. The path
must always start with a slash (to facilitate matching), and will
always be relative to the ".misaki.yaml" file. The path will always
use forward slashes, even on Windows.

Subclasses must implement this method.
"""
        raise NotImplementedError()

    def _match(self, context: dict) -> bool:
        """Caching version of :py:meth:`_match_uncached`.

Don't override this."""

        cache = context["cache"]
        result = cache.get(self, None)
        if result is None:
            cache[self] = result = self._match_uncached(context)

        return result

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return "Pattern({})".format(self.to_json())

    def to_json(self):
        """Return JSON representation of this pattern."""
        raise NotImplementedError()


class RegexPattern(BasePattern):
    def __init__(self, regex: str):
        self.regex = regex
        self.regex_ = re.compile(regex, re.S)

    def _match_uncached(self, context) -> bool:
        path = context["path"]
        return self.regex_.search(path) is not None

    def to_json(self):
        return "re:{}".format(self.regex)


class OperatorPattern(BasePattern):
    def __init__(self, operands):
        self.operands = tuple(operands)

    def to_json(self):
        return [self.operator_name] + [a.to_json() for a in self.operands]


class OrPattern(OperatorPattern):
    operator_name = "or"

    def _match_uncached(self, context) -> bool:
        return any(pat._match(context) for pat in self.operands)


class AndPattern(OperatorPattern):
    operator_name = "and"

    def _match_uncached(self, context) -> bool:
        return all(pat._match(context) for pat in self.operands)


class NotPattern(OperatorPattern):
    operator_name = "not"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.operands) != 1:
            raise ValueError("'not' operator can only take 1 argument")

    def _match_uncached(self, context) -> bool:
        return not self.operands[0]._match(context)
