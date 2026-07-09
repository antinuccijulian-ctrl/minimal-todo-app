import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = Path(__file__).with_name("tasks.json")


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimal To-Do")
        self.root.geometry("430x500")
        self.root.minsize(380, 420)
        self.root.configure(bg="#f4f4f4")

        self.tasks = self.load_tasks()
        self.dark_mode = False

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", padding=6)

        self.title_label = tk.Label(
            root,
            text="To Do",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f4f4",
            fg="#222222",
        )
        self.title_label.pack(pady=(18, 8))

        self.subtitle_label = tk.Label(
            root,
            text="Keep your day simple.",
            font=("Segoe UI", 10),
            bg="#f4f4f4",
            fg="#666666",
        )
        self.subtitle_label.pack(pady=(0, 14))

        self.input_frame = tk.Frame(root, bg="#f4f4f4")
        self.input_frame.pack(fill="x", padx=20, pady=6)

        self.task_entry = ttk.Entry(self.input_frame)
        self.task_entry.pack(side="left", fill="x", expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = ttk.Button(self.input_frame, text="Add", command=self.add_task)
        self.add_button.pack(side="left", padx=(8, 0))

        self.theme_button = ttk.Button(self.input_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_button.pack(side="left", padx=(8, 0))

        self.list_frame = tk.Frame(root, bg="#f4f4f4")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 16))

        self.listbox = tk.Listbox(
            self.list_frame,
            height=14,
            font=("Segoe UI", 11),
            bd=0,
            highlightthickness=0,
            activestyle="none",
            selectbackground="#dce8ff",
            selectforeground="#111111",
            bg="white",
        )
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.root.bind("<Delete>", lambda event: self.delete_task())

        self.button_frame = tk.Frame(root, bg="#f4f4f4")
        self.button_frame.pack(fill="x", padx=20, pady=(0, 18))

        self.delete_button = ttk.Button(self.button_frame, text="Delete", command=self.delete_task)
        self.delete_button.pack(side="left")
        self.delete_button.state(["disabled"])

        self.important_button = ttk.Button(self.button_frame, text="Mark Important", command=self.toggle_important)
        self.important_button.pack(side="left", padx=(8, 0))
        self.important_button.state(["disabled"])

        self.apply_theme()
        self.refresh_tasks()

    def load_tasks(self):
        if not DATA_FILE.exists():
            return []

        try:
            with DATA_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            return [
                {"text": item.get("text", ""), "important": bool(item.get("important", False))}
                for item in data
            ]
        except (json.JSONDecodeError, OSError, TypeError):
            return []

    def save_tasks(self):
        with DATA_FILE.open("w", encoding="utf-8") as handle:
            json.dump(self.tasks, handle, indent=2)

    def apply_theme(self):
        if self.dark_mode:
            bg = "#1f1f1f"
            fg = "#f5f5f5"
            muted = "#b6b6b6"
            entry_bg = "#2b2b2b"
            entry_fg = "#f5f5f5"
            list_bg = "#252525"
            select_bg = "#4a4a4a"
            select_fg = "#ffffff"
            border = "#3a3a3a"
        else:
            bg = "#f4f4f4"
            fg = "#222222"
            muted = "#666666"
            entry_bg = "white"
            entry_fg = "#222222"
            list_bg = "white"
            select_bg = "#dce8ff"
            select_fg = "#111111"
            border = "#d0d0d0"

        self.root.configure(bg=bg)
        self.title_label.configure(bg=bg, fg=fg)
        self.subtitle_label.configure(bg=bg, fg=muted)
        self.input_frame.configure(bg=bg)
        self.list_frame.configure(bg=bg)
        self.button_frame.configure(bg=bg)

        self.task_entry.configure(style="TEntry")
        self.task_entry.configure(background=entry_bg, foreground=entry_fg)
        self.listbox.configure(bg=list_bg, fg=fg, selectbackground=select_bg, selectforeground=select_fg, highlightbackground=border, highlightcolor=border)

        style = ttk.Style()
        style.configure("TButton", foreground=fg, background=bg)
        style.map("TButton", background=[("active", "#3f3f3f" if self.dark_mode else "#e6e6e6")])
        self.theme_button.configure(text="Light Mode" if self.dark_mode else "Dark Mode")

    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            prefix = "⭐ " if task["important"] else "• "
            self.listbox.insert(tk.END, f"{prefix}{task['text']}")

        self.listbox.selection_clear(0, tk.END)
        self.delete_button.state(["disabled"])
        self.important_button.state(["disabled"])

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Empty task", "Please enter a task first.")
            return

        self.tasks.append({"text": task_text, "important": False})
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.refresh_tasks()

    def delete_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("No task selected", "Select a task first, then press Delete.")
            return

        if not messagebox.askyesno("Delete task", "Delete the selected task?"):
            return

        index = selected[0]
        del self.tasks[index]
        self.save_tasks()
        self.refresh_tasks()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.refresh_tasks()

    def toggle_important(self):
        selected = self.listbox.curselection()
        if not selected:
            return

        index = selected[0]
        self.tasks[index]["important"] = not self.tasks[index]["important"]
        self.save_tasks()
        self.refresh_tasks()

    def on_select(self, _event):
        if self.listbox.curselection():
            self.delete_button.state(["!disabled"])
            self.important_button.state(["!disabled"])
        else:
            self.delete_button.state(["disabled"])
            self.important_button.state(["disabled"])


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
