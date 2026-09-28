import argparse

def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog = "vfs-emulator",
        description="Эмулятор командной оболочки UNIX-подобной ОС",
    )
    parser.add_argument(
        "--vfs",
        dest="vfs_path",
        default=None,
        help="Путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        dest="script_path",
        default=None,
        help="Путь к стартовому скрипту",
    )
    return parser.parse_args(argv)

def debug_print_config(config: dict) -> None:
    print("Конфигурация эмулятора")
    for key, value in config.items():
        print(f"{key} = {value}")