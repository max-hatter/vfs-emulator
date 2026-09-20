from src.gui import EmulatorGUI

def main():
    vfs_name = "my-vfs"
    app = EmulatorGUI(vfs_name=vfs_name)
    app.run()
if __name__ == "__main__":
    main()