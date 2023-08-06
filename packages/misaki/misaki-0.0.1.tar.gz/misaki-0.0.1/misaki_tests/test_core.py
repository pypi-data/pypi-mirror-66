import pytest  # noqa

from .conftest import copy_from_test_dir, run_misaki, git


def test_parse():
    # invoke misaki with invalid command argument on purpose
    assert run_misaki(["-c"]) != 0


def test_git(tmp_path_git, capsysbinary):
    #FIXME: make this an actual test
    copy_from_test_dir("git1")
    git(["add", "."])

    capsysbinary.readouterr()
    run_misaki(["--list-files", "--vc-status=tracked"])
    captured = capsysbinary.readouterr()

    # with capsysbinary.disabled():
    #     print(captured)

    git(["commit", "-m", "foo"])
