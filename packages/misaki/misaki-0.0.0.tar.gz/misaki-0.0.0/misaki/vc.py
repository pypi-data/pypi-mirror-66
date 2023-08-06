import attr
from pathlib import Path, PurePosixPath
import subprocess
from typing import List


class GitError(RuntimeError):
    pass


@attr.s
class FileStatus:
    """
Attributes
----------
workspace: Path
    Path to git repository workspace root.
path: PurePosixPath
    File path. Relative to :py:attr:`workspace`.
orig_path: PurePosixPath
    Original file path in case of a rename or copy, or
    ``None``. Relative to :py:attr:`workspace`.
vc_is_tracked: bool
    Is the file tracked by version control system?
vc_is_dirty: bool
    Does this file have modifications not saved in version control? If
    the file is not tracked, then this is always true.
vc_is_added: bool
    Would performing :py:meth:`VersionControl.vc_add` on this file do
    nothing? If the file is not tracked, then this is always false
    (since performing ``vc_add`` would add the file).
"""

    workspace = NotImplemented
    path = NotImplemented
    orig_path = NotImplemented


@attr.s
class UntrackedFileStatus(FileStatus):
    fspath: Path = attr.ib()
    orig_path = None
    orig_fspath = None

    vc_is_tracked = False
    vc_is_dirty = True
    vc_is_added = False

    @property
    def workspace(self):
        raise NotImplementedError()

    @property
    def path(self):
        raise NotImplementedError()


@attr.s
class RealFileStatus(FileStatus):
    workspace: Path = attr.ib()
    path: PurePosixPath = attr.ib()
    orig_path: PurePosixPath = attr.ib()

    @property
    def fspath(self):
        return self.workspace / Path(self.path)

    @property
    def orig_fspath(self):
        p = self.orig_path
        return self.workspace / Path(p) if p else None


@attr.s
class GitFileStatus1(RealFileStatus):
    """Git file status, parsed from git-status porcelain version 1.

Attributes
----------
git_status: str
    Two-character git file status.
"""

    git_status: str = attr.ib()

    @property
    def vc_is_tracked(self):
        return self.git_status.rstrip("?!") != ""

    @property
    def vc_is_dirty(self):
        # TODO: this likely has false positives
        return self.git_status.rstrip(" ") != ""

    @property
    def vc_is_added(self):
        if not self.vc_is_tracked:
            return False
        return (not self.vc_is_dirty) or (self.git_status[1] == " ")


class VersionControl:
    def vc_add(self, path: List[Path]):
        raise NotImplementedError()


class Git:
    def __init__(self, git_command: list, directory: Path):
        self.git_command = git_command
        self.directory = directory

    def git_check_output(self, args):
        try:
            return subprocess.check_output(
                self.git_command + args, cwd=self.directory
            )
        except subprocess.CalledProcessError as exc:
            raise GitError("failed to call git") from exc

    @property
    def vc_workspace_path(self) -> Path:
        output = self.git_check_output(["rev-parse", "--show-toplevel"])

        # TODO: handle corner case where path legitimately ends in a
        # newline char (as you may imagine, very low priority)
        path = Path(output.decode("utf-8").rstrip("\n\r"))

        if not path.is_dir():
            raise AssertionError(
                "git toplevel directory {!r} doesn't exist?".format(path)
            )

        return path

    def vc_status(self):
        files = {}

        workspace = self.vc_workspace_path

        # get list of files git knows about
        output = self.git_check_output(["ls-files", "-z"])
        for line in output.split(b"\0"):
            if not line:
                continue

            file_path = line.decode("utf-8", errors="surrogateescape")
            files[file_path] = GitFileStatus1(
                git_status="  ",  # clean
                workspace=workspace,
                path=PurePosixPath(file_path),
                orig_path=None,
            )

        # get file info on files that are not in a clean state
        output = self.git_check_output(["status", "--porcelain=v1", "-z"])

        line_iter = iter(output.split(b"\0"))
        for line in line_iter:
            if not line:
                continue

            file_status = line[:2]
            file_path = line[3:]
            if line[2:3] != b" ":
                raise AssertionError("cannot parse line {!r}".format(line))

            file_status = file_status.decode("ascii")
            file_path = file_path.decode("utf-8", errors="surrogateescape")

            file_orig_path = None

            if "R" in file_status or "C" in file_status:
                # get rename or copy source
                file_orig_path = next(line_iter).decode(
                    "utf-8", errors="surrogateescape"
                )

            files[file_path] = GitFileStatus1(
                git_status=file_status,
                workspace=workspace,
                path=PurePosixPath(file_path),
                orig_path=(
                    PurePosixPath(file_orig_path) if file_orig_path else None
                ),
            )

        return files

    def vc_add(self, paths):
        for path in paths:
            self.git_check_output(["add", "-f", "--", str(path)])
