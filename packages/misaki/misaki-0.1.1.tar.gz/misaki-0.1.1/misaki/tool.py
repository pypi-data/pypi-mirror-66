import json
from pathlib import Path
import subprocess
import sys
from typing import List

from .file import File
from .util import get_path


class Tool:
    """Tool.

Attributes
----------
misaki: :py:class:`~misaki.app.Misaki`
    Misaki application instance.
tool_id:
    String identifying this tool instance.
"""

    order = 0
    destructive = True

    def __init__(self, misaki, tool_id: str):
        self.misaki = misaki
        self.tool_id = tool_id

    @property
    def config(self):
        return self.misaki.config["tools"][self.tool_id]

    def run(self, files: List[File]) -> int:
        raise NotImplementedError()

    @property
    def dry_run(self):
        return self.misaki.dry_run

    def to_json(self):
        return {"class": str(type(self))}

    def __hash__(self):
        return hash(self.tool_id)

    def __eq__(self, other):
        return self is other


class CommandMixin:
    def get_command(self):
        cmd = get_path(self.config, "command.command", self.default_command)

        if isinstance(cmd, str):
            cmd = [cmd]

        return cmd

    def stringify_command_args(self, args):
        result = []
        for arg in args:
            if isinstance(arg, str):
                pass
            elif isinstance(arg, bytes):
                arg = arg.decode("utf-8", errors="surrogateescape")
            elif isinstance(arg, Path):
                arg = str(arg.path)
            elif isinstance(arg, File):
                arg = str(Path(*arg.path.parts))
            else:
                raise TypeError("can't handle {!r}".format(arg))

            result.append(arg)

        return result

    def run(self, files) -> int:
        return self.command_run_xargs(files)

    def command_run_xargs(self, files) -> int:
        if not files:
            return  # no point

        # FIXME: cmdline arg limit

        args = self.construct_command_args(files)
        args = self.stringify_command_args(args)

        exitcode = self.command_run(args)
        if exitcode != 0:
            print(
                "command {!r} exited with status code {}".format(
                    args, exitcode
                ),
                file=sys.stderr,
            )

        return exitcode

    def command_popen(self, args, **kw):
        return subprocess.Popen(args, cwd=self.misaki.root, **kw)

    def command_run(self, args) -> int:
        if self.dry_run:
            tree = {"!": "run_command", "command": args}
            print(json.dumps(tree, indent=2))
            return 0

        proc = self.command_popen(args)
        return proc.wait()


class Formatter(Tool):
    order = 1000
    destructive = True


class Linter(Tool):
    order = 2000
    destructive = False


class NullTool(Tool):
    pass
