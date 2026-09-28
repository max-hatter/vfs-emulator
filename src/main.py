from src.config import parse_args, debug_print_config
from src.gui import EmulatorGUI


def main():
    args = parse_args()
    config = {
        "vfs_path": args.vfs_path,
        "script_path": args.script_path,
    }

    debug_print_config(config)

    import os
    if config["vfs_path"]:
        vfs_name = os.path.basename(config["vfs_path"])
    else:
        vfs_name = "my-vfs"

    app = EmulatorGUI(vfs_name=vfs_name, config=config)
    app.run()


if __name__ == "__main__":
    main()