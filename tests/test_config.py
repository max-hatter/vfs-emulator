from src.config import parse_args


def test_no_args():
    args = parse_args([])
    assert args.vfs_path is None
    assert args.script_path is None


def test_vfs_only():
    args = parse_args(["--vfs", "data/vfs.csv"])
    assert args.vfs_path == "data/vfs.csv"
    assert args.script_path is None


def test_script_only():
    args = parse_args(["--script", "scripts/startup.txt"])
    assert args.vfs_path is None
    assert args.script_path == "scripts/startup.txt"


def test_both_args():
    args = parse_args(["--vfs", "a.csv", "--script", "b.txt"])
    assert args.vfs_path == "a.csv"
    assert args.script_path == "b.txt"