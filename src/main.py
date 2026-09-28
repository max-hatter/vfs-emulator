from src.config import parse_args, debug_print_config
from src.gui import EmulatorGUI


def main():
    # 1. Разбираем аргументы командной строки
    args = parse_args()
    config = {
        "vfs_path": args.vfs_path,
        "script_path": args.script_path,
    }

    # 2. Отладочный вывод параметров
    debug_print_config(config)

    # 3. Определяем имя VFS для заголовка окна
    import os
    if config["vfs_path"]:
        vfs_name = os.path.basename(config["vfs_path"])
    else:
        vfs_name = "my-vfs"

    # 4. Создаём GUI и передаём ему конфиг
    app = EmulatorGUI(vfs_name=vfs_name, config=config)
    app.run()


if __name__ == "__main__":
    main()