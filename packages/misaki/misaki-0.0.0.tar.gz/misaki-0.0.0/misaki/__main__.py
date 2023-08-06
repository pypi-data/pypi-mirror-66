import pathlib

import argh
from argh import expects_obj, arg

from .app import Misaki, VCStatusRule


@arg(
    "--config",
    "-c",
    type=pathlib.Path,
    action="append",
    help="Override configuration file. Normally, this tool just looks for "
    "a file called '.misaki.yaml' in parents of the current directory.",
)
@arg("--run-linters", action="store_true", help="Run all defined linters.")
@arg(
    "--run-formatters",
    action="store_true",
    help="Run all defined code formatters.",
)
@arg(
    "--dry-run",
    "-n",
    action="store_true",
    help="Don't actually run any commands, "
    "only print out what would be done.",
)
@arg(
    "--list-files", action="store_true", help="List files according to filter."
)
@arg(
    "--print-config",
    action="store_true",
    help="Print effective configuration in JSON format, as perceived by Misaki.",
)
@arg(
    "--vc-status",
    action="append",
    metavar="RULE",
    type=VCStatusRule.from_string,
    help="Filter by version control status attributes. For example, to "
    "include files that are tracked by version control but haven't been "
    "modified (aren't 'dirty'), use `--vc-status='tracked,!dirty'`. This "
    "option can be specified multiple times.",
)
@arg(
    "--vc-changed",
    action="store_true",
    help="Equivalent to `--vc-status=tracked,dirty`.",
)
@arg(
    "--no-vc-add",
    action="store_true",
    help="Files that are tracked in version control that are modified by tools "
    "(e.g., formatters) are, by default, re-added to version control. "
    "Use this option to inhibit this behavior.",
)
@arg(
    "--pattern",
    action="append",
    help="Specify file pattern. Can be specified multiple times.",
)
@arg("--run", action="append", help="Run tool.")
@arg(
    "--set",
    action="append",
    help="Set configuration option, "
    "e.g. `--set=flake8.config.show-source=true`.",
)
@expects_obj
def main_command(obj):
    # print(obj)
    exit(Misaki.from_argh(obj))


def main(**kwargs):
    argh.dispatch_command(main_command, **kwargs)


if __name__ == "__main__":
    main()
