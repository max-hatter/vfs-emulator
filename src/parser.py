import os
import shlex

def expand_env_vars(text: str) -> str:
    return os.path.expandvars(text)

def parse_command(line: str) -> tuple[str, list[str]]:
    line = expand_env_vars(line.strip())
    if not line:
        return "", []
    try:
        parts = shlex.split(line)
    except ValueError as e:
        raise ValueError(f"Ошибка разбора строки: {e}")
    if not parts:
        return "", []
    return parts[0], parts[1:]