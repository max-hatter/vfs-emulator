import os
import shlex

def expand_env_vars(text: str) -> str:
    if os.name == "nt" and "HOME" not in os.environ:
        profile = os.environ.get("USERPROFILE", "")
        if profile:
            text = text.replace("$HOME", profile).replace("${HOME}", profile)
    return os.path.expandvars(text)

def _strip_quotes(token: str) -> str:
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ('"', "'"):
        return token[1:-1]
    return token

def parse_command(line: str) -> tuple[str, list[str]]:
    line = expand_env_vars(line.strip())
    if not line:
        return "", []
    try:
        parts = shlex.split(line, posix=False)
    except ValueError as e:
        raise ValueError(f"Ошибка разбора строки: {e}")
    parts = [_strip_quotes(p) for p in parts]
    if not parts:
        return "", []
    return parts[0], parts[1:]