import json
import os
import yaml
from pathlib import Path
from typing import Dict, Iterable

import attr

from .file import File
from .pattern import Patterns
from .tool import Formatter, Linter
from .util import import_object
from .vc import Git, FileStatus, UntrackedFileStatus


VERSION = 0


PREDEFINED_TOOL_CLASSES = {
    "black": ".ext.black.Black",
    "flake8": ".ext.flake8.Flake8",
    "isort": ".ext.isort.ISort",
    "null": ".tool.NullTool",
}

DEFAULT_IGNORE_PATTERN = r"re:/\."  # match any files with leading dot


def apply_delta(result, delta):
    for k, v in delta.items():
        if isinstance(v, dict):
            if k in result:
                apply_delta(result[k], v)
            else:
                result[k] = v
        else:
            result[k] = v


@attr.s
class VCStatusRule:
    _vc_status_attributes = {"dirty", "tracked", "added"}

    conditions: Dict[str, bool] = attr.ib()

    @classmethod
    def from_string(cls, string):
        conditions = {}
        for condition in string.split(","):
            if condition.startswith("!"):
                value = False
                condition = condition[1:]
            else:
                value = True

            if condition not in cls._vc_status_attributes:
                raise ValueError(
                    "unknown version control attribute {!r}".format(condition)
                )

            conditions[condition] = value

        return cls(conditions)

    def match(self, vc_status: FileStatus) -> bool:
        return all(
            getattr(vc_status, "vc_is_" + k) == v
            for k, v in self.conditions.items()
        )


class Misaki:
    """Main class that does things.

Attributes
----------
root: :py:class:`pathlib.Path`
    Root Misaki directory.
patterns: dict
    Patterns.
tools: dict
    Tools.
config: dict
    Configuration, nested JSON data.
flag_vc_re_add_files: bool
    Re-add files to version control that were modified by tools.
"""

    vc = None
    dry_run = True
    flag_vc_re_add_files = False

    @classmethod
    def from_argh(cls, obj):
        misaki = cls()
        misaki.init_argh(obj)
        return misaki.main_argh(obj)

    def init_argh(self, obj):
        # If the user specified `-c CONFIGFILE`, use it.
        if obj.config:
            config_files = obj.config
        else:
            config_files = self.find_config_files()
            if not config_files:
                raise FileNotFoundError("could not find `.misaki.yaml` file")

        self.dry_run = obj.dry_run

        self.vc_rules = obj.vc_status or []

        if obj.vc_changed:
            self.vc_rules.append(VCStatusRule.from_string("dirty,tracked"))

        self.flag_vc_re_add_files = not obj.no_vc_add

        self.init_config(config_files)

        if self.vc_rules:
            self.init_vc()

        self.init_tools()

        # user specified --pattern, filter by that
        if obj.pattern:
            ignore_redefinition = {
                "or": ["__ignore__", {"not": [{"or": ["re:/$"] + obj.pattern}]}]
            }
            self.patterns.parse_definitions(
                [{"__ignore__": ignore_redefinition}]
            )

    def main_argh(self, obj):
        if obj.print_config:
            print(
                json.dumps(
                    {
                        "patterns": {
                            name: pat.to_json()
                            for name, pat in self.patterns.patterns.items()
                        },
                        "tools": {
                            name: tool.to_json()
                            for name, tool in self.tools.items()
                        },
                        "config": self.config,
                    },
                    indent=2,
                )
            )
            return 0

        self.relevant_files = self.get_relevant_files()

        if obj.list_files:
            print(
                json.dumps(
                    {
                        "root": str(self.root),
                        "files": [
                            file.to_json() for file in self.relevant_files
                        ],
                    },
                    indent=2,
                )
            )
            return 0

        run_ = obj.run if obj.run else []

        run = set()
        for tool_id in run_:
            tool = self.tools.get(tool_id, None)
            if tool is None:
                raise KeyError("unknown tool {!r}".format(tool_id))
            run.add(tool)

        # fmt: off
        if obj.run_linters:
            run.update(
                tool for tool in self.tools.values()
                if isinstance(tool, Linter)
            )
        if obj.run_formatters:
            run.update(
                tool for tool in self.tools.values()
                if isinstance(tool, Formatter)
            )
        # fmt: on

        run = list(sorted(run, key=lambda tool: tool.order))

        files_in_pattern = {}
        for file in self.relevant_files:
            for pattern_id, is_match in self.patterns.evaluate_patterns(
                file
            ).items():
                if not is_match:
                    continue
                files = files_in_pattern.get(pattern_id, None)
                if files is None:
                    files_in_pattern[pattern_id] = files = []
                files.append(file)

        exit_code = 0
        for tool in run:
            files = list(
                sorted(files_in_pattern.get(tool.config["pattern"], []))
            )
            try:
                exit_code += tool.run(files) != 0
            finally:
                if self.vc and self.flag_vc_re_add_files:
                    self.vc.vc_add(
                        [
                            file.fspath
                            for file in files
                            if file.vc_status.vc_is_added
                        ]
                    )

        return exit_code + 100 if exit_code else 0

    def init_vc(self):
        vc = Git(["git"], self.root)
        try:
            vc.vc_workspace_path
        except Exception:
            vc = None

        self.vc = vc

    def get_relevant_files(self) -> Dict[str, Path]:
        result = []
        for file in self.get_all_files():
            if all(vc_rule.match(file.vc_status) for vc_rule in self.vc_rules):
                result.append(file)
        return result

    def apply_vc_info(self, files: Iterable[File]) -> None:
        """Get version control system information and apply it to
:py:class:`File` objects."""

        if self.vc is not None:
            statuses = self.vc.vc_status()
            statuses = {st.fspath: st for st in statuses.values()}
        else:
            statuses = {}

        for file in files:
            st = statuses.get(file.fspath, None)
            if st is not None:
                file.vc_status = st
            else:
                file.vc_status = UntrackedFileStatus(file.fspath)

    def get_all_files(self) -> Dict[str, Path]:
        """Get all files."""
        ignore_pattern = self.patterns.patterns["__ignore__"]

        result = []
        misaki_root = self.root
        for root, dirs, files in os.walk(
            misaki_root, topdown=True, followlinks=False
        ):
            root = Path(root)
            for f in files:
                absolute_path = root / f
                file = File.from_fspath(
                    fspath=absolute_path, misaki_root=misaki_root
                )
                if file is None:
                    continue
                if not ignore_pattern.match(file.path):
                    result.append(file)

            old_dirs = dirs.copy()
            dirs.clear()
            for f in old_dirs:
                absolute_path = root / f
                file = File.from_fspath(
                    fspath=absolute_path, misaki_root=misaki_root
                )
                if file is None:
                    continue
                if not ignore_pattern.match(str(file.path) + "/"):
                    dirs.append(f)

        self.apply_vc_info(result)

        return result

    def init_config(self, config_files):
        self.patterns = pp = Patterns()
        self.config = config = {"tools": {}}

        # We deduce the misaki root based on the config_files.
        self.root = config_files[0].parent.resolve()

        pp.parse_definitions([{"__ignore__": DEFAULT_IGNORE_PATTERN}])

        for config_file in config_files:

            with open(str(config_file), "rt", encoding="utf-8") as file:
                cfg = yaml.load(file)

            pp.parse_definitions(cfg.get("patterns", []))

            apply_delta(config["tools"], cfg.get("tools", {}))

    def init_tools(self):
        self.tools = {}

        for tool_id, tool_dict in self.config["tools"].items():
            cls = tool_dict.get("class", None)
            if not cls:
                cls = PREDEFINED_TOOL_CLASSES.get(tool_id, None)
            if not cls:
                raise KeyError(
                    'did not specify "class" for tool {!r}'.format(cls)
                )
            cls = import_object(cls, __name__)
            self.tools[tool_id] = cls(misaki=self, tool_id=tool_id)

    def find_config_files(self):
        current = Path(".").resolve()
        dirs = [current] + list(current.parents)
        for path in dirs:
            config_file = path / ".misaki.{}.yaml".format(VERSION)
            if config_file.exists():
                break
        else:
            return []

        files = [config_file]
        local_config_file = path / ".misaki.{}.local.yaml".format(VERSION)
        if local_config_file.exists():
            files.append(local_config_file)

        return files
