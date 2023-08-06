import os
import subprocess

from .conftest import git, writestring
from misaki.vc import Git

GIT_RENAME_WORKS = True


def test_git_statuses(tmp_path_git):
    G = Git(["git"], tmp_path_git)

    A20 = "A\n" * 20
    A19B = "A\n" * 19 + "B\n"

    # write a file, check that git-status sees it
    writestring("a.txt", A20)

    st, = G.vc_status().values()
    assert str(st.path) == "a.txt"
    assert st.orig_path is None
    assert st.fspath == st.workspace / "a.txt"
    assert st.vc_is_dirty is True
    assert st.vc_is_added is False
    assert st.vc_is_tracked is False

    # add the file to the git index aka staging area
    G.vc_add([st.fspath])

    st, = G.vc_status().values()
    assert st.vc_is_dirty is True
    assert st.vc_is_added is True

    # modify the file in the work tree while it's already staged
    writestring("a.txt", A19B)

    st, = G.vc_status().values()
    assert st.vc_is_dirty is True
    assert st.vc_is_added is False

    # commit the staged version, keeping the work tree copy dirty
    git(["commit", "-m", "a"])

    st, = G.vc_status().values()
    assert st.vc_is_dirty is True
    assert st.vc_is_added is False

    # restore clean working tree copy
    git(["checkout", "--", "a.txt"])

    st, = G.vc_status().values()
    assert st.vc_is_dirty is False
    assert st.vc_is_added is True

    # rename the file, and stage change
    os.rename("a.txt", "b.txt")
    G.vc_add(["a.txt", "b.txt"])

    if GIT_RENAME_WORKS:
        st, = G.vc_status().values()
        assert str(st.path) == "b.txt"
        assert str(st.orig_path) == "a.txt"
        assert st.vc_is_dirty is True
        assert st.vc_is_added is True

    git(["commit", "-m", "b"])

    st, = G.vc_status().values()
    assert str(st.path) == "b.txt"
    assert st.vc_is_dirty is False
    assert st.vc_is_added is True


def test_git_merge(tmp_path_git):
    G = Git(["git"], tmp_path_git)

    A20 = "A\n" * 20
    A19B = "A\n" * 19 + "B\n"
    A19C = "A\n" * 19 + "C\n"

    # base version
    writestring("a", A20)
    G.vc_add(["a"])
    git(["checkout", "-b", "base"])
    git(["commit", "-m", "a"])

    # branch-b
    writestring("a", A19B)
    G.vc_add(["a"])
    git(["checkout", "-b", "branch-b"])
    git(["commit", "-m", "b"])

    # branch-c
    git(["checkout", "base"])  # checkout base version
    writestring("a", A19C)  # create merge conflict
    G.vc_add(["a"])
    git(["checkout", "-b", "branch-c"])
    git(["commit", "-m", "c"])

    # create conflict by merging branch-b into branch-c
    try:
        git(["merge", "--no-commit", "branch-b"])
    except subprocess.CalledProcessError:
        pass

    st, = G.vc_status().values()
    assert st.vc_is_dirty is True
    assert st.vc_is_added is False

    # resolve conflict by picking branch-b version (different from original)
    writestring("a", A19B)
    G.vc_add(["a"])

    st, = G.vc_status().values()
    assert st.vc_is_dirty is True
    assert st.vc_is_added is True

    # resolve conflict by picking branch-c version (original version)
    writestring("a", A19C)
    G.vc_add(["a"])

    st, = G.vc_status().values()
    assert st.vc_is_dirty is False
    assert st.vc_is_added is True
