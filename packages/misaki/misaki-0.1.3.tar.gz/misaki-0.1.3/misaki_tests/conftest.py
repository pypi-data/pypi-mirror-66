import json
import os
import subprocess

import pytest

from misaki.__main__ import main


def run_misaki(argv):
    try:
        main(argv=argv)
    except SystemExit as exc:
        return exc.code

    return 0


@pytest.fixture(scope="function")
def capture_json_stdout(capsysbinary):
    def call(function):
        capsysbinary.readouterr()
        ret = function()
        out, err = capsysbinary.readouterr()
        return (ret, json.loads(out))

    return call


def writestring(path, string):
    with open(path, "wt", encoding="utf-8") as file:
        file.write(string)


def readstring(path):
    with open(path, "rt", encoding="utf-8") as file:
        return file.read()


# def copy_from_test_dir(name):
#     a = pathlib.Path(__file__).parent / name
#     for p in a.iterdir():
#         if p.is_dir():
#             shutil.copytree(str(p), p.name)
#         else:
#             shutil.copy(str(p), p.name)


git_command = ["git"]


def git(args):
    return subprocess.check_output(git_command + args)


@pytest.fixture(scope="function")
def tmp_path_chdir(tmpdir):
    os.chdir(str(tmpdir))
    yield tmpdir


@pytest.fixture(scope="function")
def tmp_path_git(tmp_path_chdir):
    git(["init"])
    yield tmp_path_chdir
