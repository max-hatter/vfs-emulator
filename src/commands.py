from abc import ABC, abstractmethod


class Command(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, args: list[str], context: dict) -> str:
        ...


class LsCommand(Command):
    name = "ls"
    description = "Список файлов в директории"

    def execute(self, args: list[str], context: dict) -> str:
        vfs = context.get("vfs")
        if vfs is None:
            return "ls: VFS не загружена"
        target = args[0] if args else vfs.cwd
        try:
            entries = vfs.list_dir(target)
        except (FileNotFoundError, NotADirectoryError) as e:
            return f"ls: {e}"
        return "\n".join(entries) if entries else ""


class CdCommand(Command):
    name = "cd"
    description = "Сменить директорию"

    def execute(self, args: list[str], context: dict) -> str:
        vfs = context.get("vfs")
        if vfs is None:
            return "cd: VFS не загружена"
        target = args[0] if args else "/"
        try:
            vfs.change_dir(target)
        except (FileNotFoundError, NotADirectoryError) as e:
            return f"cd: {e}"
        return ""


class ExitCommand(Command):
    name = "exit"
    description = "Выход из эмулятора"

    def execute(self, args: list[str], context: dict) -> str:
        if args:
            return "exit: команда не принимает аргументов"
        context["exit"] = True
        return "Завершение работы..."


COMMANDS: dict[str, Command] = {
    "ls": LsCommand(),
    "cd": CdCommand(),
    "exit": ExitCommand(),
}


def execute_command(name: str, args: list[str], context: dict) -> str:
    if name not in COMMANDS:
        return f"Ошибка: неизвестная команда '{name}'"
    try:
        return COMMANDS[name].execute(args, context)
    except Exception as e:
        return f"Ошибка выполнения '{name}': {e}"