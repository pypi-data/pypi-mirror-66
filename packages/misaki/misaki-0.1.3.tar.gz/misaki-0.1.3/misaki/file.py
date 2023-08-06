import attr
from pathlib import Path, PurePosixPath
from .vc import FileStatus


@attr.s
class File:
    """
Attributes
----------
path: :py:class:`PurePosixPath`
    Standardized UNIX-style filename relative to Misaki root
    directory.
fspath: :py:class:`Path`
    Actual file on disk. Computed from :py:attr:`path` and
    :py:attr:`misaki_root`.
misaki_root: :py:class:`pathlib.Path`
    Misaki root.
vc_status: :py:class:`FileStatus`
    Version control status, or ``None``.
"""

    path: PurePosixPath = attr.ib()
    misaki_root: Path = attr.ib()
    vc_status: FileStatus = attr.ib(default=None)

    @classmethod
    def from_fspath(cls, fspath, misaki_root, **kw):
        root_parts = misaki_root.parts
        path_parts = fspath.parts
        n = len(root_parts)

        if path_parts[:n] == root_parts:
            return cls(
                path=PurePosixPath("/".join(path_parts[n:])),
                misaki_root=misaki_root,
                **kw
            )
        else:
            return None

    @property
    def fspath(self):
        return self.misaki_root / Path(self.path)

    def __str__(self):
        return str(self.path)

    def to_json(self):
        st = self.vc_status
        return {
            "path": str(self.path),
            "vc_is_dirty": st.vc_is_dirty if st else True,
            "vc_is_added": st.vc_is_added if st else False,
            "vc_is_tracked": st.vc_is_tracked if st else False,
        }
