import pytest  # noqa

from .conftest import run_misaki, git, readstring, writestring


def test_cmdline_fail():
    # invoke misaki with invalid command argument on purpose
    assert run_misaki(["-c"]) != 0


misaki0_python_cfg = r"""
patterns:
  - __ignore__:
      or:
        - __ignore__
        - 're:/\.'
  - python: 're:\.pyi?$'

tools:
  black:
    config:
      line-length: 80
    pattern: "python"
  flake8:
    pattern: "flake8"
"""

flake8_cfg = r"""
[flake8]
max-line-length = 80
select = C,E,F,W,B,B950
ignore = E203,E501,W503
"""

noncompliant_python = r"""
from os import path # unused import
print(
(((x)))+     y)
"""


def test_git(tmp_path_git, capsysbinary, capture_json_stdout):
    writestring(".misaki.0.yaml", misaki0_python_cfg)
    writestring(".flake8", flake8_cfg)
    writestring("a.py", noncompliant_python)

    exitcode, out = capture_json_stdout(
        lambda: run_misaki(["--list-files", "--vc-status=tracked"])
    )
    assert exitcode == 0
    assert not out["files"]

    exitcode, out = capture_json_stdout(
        lambda: run_misaki(["--list-files", "--vc-status=dirty"])
    )
    assert exitcode == 0
    assert out["files"][0] == {
        "path": "a.py",
        "vc_is_dirty": True,
        "vc_is_added": False,
        "vc_is_tracked": False,
    }

    # run linter, should fail
    exitcode = run_misaki(["--run-linters", "--vc-status=dirty"])
    assert exitcode == 101

    # run formatter
    exitcode = run_misaki(["--run-formatters", "--vc-status=dirty"])
    assert exitcode == 0
    assert readstring("a.py") != noncompliant_python

    # git add a.py
    writestring("a.py", noncompliant_python)
    git(["add", "a.py"])

    exitcode = run_misaki(["--run-formatters", "--vc-changed"])
    assert readstring("a.py") != noncompliant_python

    exitcode, out = capture_json_stdout(
        lambda: run_misaki(["--list-files", "--vc-changed"])
    )
    assert exitcode == 0
    assert out["files"][0] == {
        "path": "a.py",
        "vc_is_dirty": True,
        "vc_is_added": True,
        "vc_is_tracked": True,
    }

    # make work tree differ from index
    writestring("a.py", noncompliant_python + "# poop\n")

    exitcode, out = capture_json_stdout(
        lambda: run_misaki(["--list-files", "--vc-changed"])
    )
    assert exitcode == 0
    assert out["files"][0] == {
        "path": "a.py",
        "vc_is_dirty": True,
        "vc_is_added": False,
        "vc_is_tracked": True,
    }
