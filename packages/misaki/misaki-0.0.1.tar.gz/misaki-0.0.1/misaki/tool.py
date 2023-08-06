import json
from subprocess import check_call

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
    def run(self, files):
        raise NotImplementedError()

    def run_command_xargs(self, files, args):
        files_ = [str(f) for f in files]
        args = list(args)

        if not files_:
            return  # no point

        # FIXME: cmdline arg limit
        self.run_command(args + files_)

    def run_command(self, args):
        command = get_path(self.config, "command.command", self.default_command)

        if isinstance(command, str):
            command = [command]
        else:
            command = list(command)

        final_command = command + args

        if self.dry_run:
            tree = {"!": "run_command", "command": final_command}
            print(json.dumps(tree, indent=2))
            return

        check_call(command + args, cwd=self.misaki.root)


class Formatter(Tool):
    order = 1000
    destructive = True


class Linter(Tool):
    order = 2000
    destructive = False


class NullTool(Tool):
    pass
