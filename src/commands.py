from abc import ABC, abstractmethod

class Command(ABC):
    name: str = ""
    description: str = ""
    @abstractmethod
    def execute(self, args: list[str], context: dict) -> str:
        ...

class LsCommand(Command):
    name = "ls"
    description = "Список файлов (заглушка)"
    def execute(self, args: list[str], context: dict) -> str:
        return f"ls: команда-заглушка, аргументы: {args}"

class CdCommand(Command):
    name = "cd"
    description = "Смена директории (заглушка)"
    def execute(self, args: list[str], context: dict) -> str:
        return f"cd: команда-заглушка, аргументы: {args}"

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