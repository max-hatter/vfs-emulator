import pytest
from src.parser import parse_command

def test_simple_command():
    name, args = parse_command("ls -la /tmp")
    assert name == "ls"
    assert args == ["-la", "/tmp"]
def test_quotes():
    name, args = parse_command('echo "hello world" \'foo bar\'')
    assert name == "echo"
    assert args == ["hello world", "foo bar"]
def test_env_var_expansion(monkeypatch):
    monkeypatch.setenv("MYTESTVAR", "/some/path")
    name, args = parse_command("cd $MYTESTVAR")
    assert name == "cd"
    assert args == ["/some/path"]
def test_empty_line():
    name, args = parse_command("   ")
    assert name == ""
    assert args == []
def test_unbalanced_quotes():
    with pytest.raises(ValueError):
        parse_command('echo "unterminated')