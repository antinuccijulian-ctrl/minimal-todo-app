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

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", padding=6)

        title = tk.Label(
            root,
            text="To Do",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f4f4",
            fg="#222222",
        )
        title.pack(pady=(18, 8))

        subtitle = tk.Label(
            root,
            text="Keep your day simple.",
            font=("Segoe UI", 10),
            bg="#f4f4f4",
            fg="#666666",
        )
        subtitle.pack(pady=(0, 14))

        input_frame = tk.Frame(root, bg="#f4f4f4")
        input_frame.pack(fill="x", padx=20, pady=6)

        self.task_entry = ttk.Entry(input_frame)
        self.task_entry.pack(side="left", fill="x", expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        add_button = ttk.Button(input_frame, text="Add", command=self.add_task)
        add_button.pack(side="left", padx=(8, 0))

        list_frame = tk.Frame(root, bg="#f4f4f4")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 16))

        self.listbox = tk.Listbox(
            list_frame,
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

        button_frame = tk.Frame(root, bg="#f4f4f4")
        button_frame.pack(fill="x", padx=20, pady=(0, 18))

        self.delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_task)
        self.delete_button.pack(side="left")
        self.delete_button.state(["disabled"])

        self.important_button = ttk.Button(button_frame, text="Mark Important", command=self.toggle_important)
        self.important_button.pack(side="left", padx=(8, 0))
        self.important_button.state(["disabled"])

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
            return

        index = selected[0]
        del self.tasks[index]
        self.save_tasks()
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
