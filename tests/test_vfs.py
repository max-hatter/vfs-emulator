import os
import tempfile

import pytest

from src.vfs import VFS


def _make_csv(content: str) -> str:
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    )
    f.write(content)
    f.close()
    return f.name


def test_load_minimal():
    path = _make_csv(
        "path,type,content\n"
        "/,dir,\n"
        "readme.txt,file,SGVsbG8=\n"
    )
    try:
        vfs = VFS()
        vfs.load_from_csv(path)
        assert vfs.exists("/")
        assert vfs.exists("/readme.txt")
        assert vfs.read_file("/readme.txt") == b"Hello"
    finally:
        os.unlink(path)


def test_list_dir():
    path = _make_csv(
        "path,type,content\n"
        "/,dir,\n"
        "a.txt,file,\n"
        "b.txt,file,\n"
    )
    try:
        vfs = VFS()
        vfs.load_from_csv(path)
        entries = vfs.list_dir("/")
        assert "a.txt" in entries
        assert "b.txt" in entries
    finally:
        os.unlink(path)


def test_nested_dirs():
    path = _make_csv(
        "path,type,content\n"
        "/,dir,\n"
        "/home,dir,\n"
        "/home/user,dir,\n"
        "/home/user/file.txt,file,SGVsbG8=\n"
    )
    try:
        vfs = VFS()
        vfs.load_from_csv(path)
        assert vfs.is_dir("/home/user")
        assert vfs.is_file("/home/user/file.txt")
    finally:
        os.unlink(path)


def test_change_dir():
    path = _make_csv(
        "path,type,content\n"
        "/,dir,\n"
        "/home,dir,\n"
        "/home/user,dir,\n"
    )
    try:
        vfs = VFS()
        vfs.load_from_csv(path)
        vfs.change_dir("/home/user")
        assert vfs.cwd == "/home/user"
        vfs.change_dir("..")
        assert vfs.cwd == "/home"
    finally:
        os.unlink(path)


def test_missing_file():
    vfs = VFS()
    with pytest.raises(FileNotFoundError):
        vfs.load_from_csv("/no/such/file.csv")


def test_bad_header():
    path = _make_csv("wrong,columns,here\na,b,c\n")
    try:
        vfs = VFS()
        with pytest.raises(ValueError):
            vfs.load_from_csv(path)
    finally:
        os.unlink(path)


def test_bad_type():
    path = _make_csv(
        "path,type,content\n"
        "/,dir,\n"
        "/x,unknown,\n"
    )
    try:
        vfs = VFS()
        with pytest.raises(ValueError):
            vfs.load_from_csv(path)
    finally:
        os.unlink(path)