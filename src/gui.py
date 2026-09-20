import tkinter as tk
from tkinter import scrolledtext
from src.parser import parse_command
from src.commands import execute_command

class EmulatorGUI:
    def __init__(self, vfs_name: str = "default-vfs"):
        self.vfs_name = vfs_name
        self.context = {"exit": False, "vfs_name": vfs_name}
        self.root = tk.Tk()
        self.root.title(vfs_name)
        self.root.geometry("800x600")
        self.output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 11)
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(
            self.root, textvariable=self.input_var, font=("Consolas", 11)
        )
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.entry.bind("<Return>", self.on_enter)
        self.print_output(f"Эмулятор VFS: {vfs_name}")
        self.print_output("Введите 'exit' для выхода.\n")
    def print_output(self, text: str):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)
    def on_enter(self, event=None):
        line = self.input_var.get()
        self.input_var.set("")
        if not line.strip():
            return
        self.print_output(f"> {line}")
        try:
            name, args = parse_command(line)
        except ValueError as e:
            self.print_output(str(e))
            return
        if not name:
            return
        result = execute_command(name, args, self.context)
        if result:
            self.print_output(result)
        if self.context.get("exit"):
            self.root.after(300, self.root.destroy)
    def run(self):
        self.entry.focus_set()
        self.root.mainloop()