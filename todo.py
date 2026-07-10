import json
import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# When running as a PyInstaller one-file exe, resources are unpacked
# to a temp dir and __file__ won't point to the application folder.
# Use the executable location when frozen, otherwise use the source file.
if getattr(sys, "frozen", False):
    # When frozen by PyInstaller, resources are available under _MEIPASS
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    # Use per-user AppData for persistent data so the one-file exe doesn't lose tasks
    appdata = os.getenv("APPDATA") or Path.home()
    DATA_DIR = Path(appdata) / "Minimal To-Do"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE = DATA_DIR / "tasks.json"
else:
    RESOURCE_DIR = Path(__file__).parent
    DATA_FILE = RESOURCE_DIR / "tasks.json"


class TodoApp:
    def __init__(self, root):
        self.root = root
        # remove native title bar so we can draw a custom one (allows coloring)
        self.root.overrideredirect(True)
        self.root.title("Minimal To-Do")
        self.root.geometry("360x460")
        self.root.minsize(340, 390)
        self.root.configure(bg="#ffffff")

        self.tasks = self.load_tasks()
        self.dark_mode = False

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", padding=6)

        # Custom title bar (replaces native OS title bar so we can color it)
        self.title_bar = tk.Frame(root, bg="#111111", relief="flat", height=32)
        self.title_bar.pack(fill="x")

        # Load the app icon PNG to show in the custom title bar
        icon_loaded = False
        icon_path = RESOURCE_DIR.joinpath("assets", "icon.png")
        if icon_path.exists():
            try:
                _icon_img = tk.PhotoImage(file=str(icon_path))
                self.title_icon = tk.Label(self.title_bar, image=_icon_img, bg="#111111")
                self.title_icon.image = _icon_img
                icon_loaded = True
            except Exception:
                icon_loaded = False

        if not icon_loaded:
            self.title_icon = tk.Label(self.title_bar, text="🗒️", bg="#111111", fg="#ffffff")

        # set window icon for taskbar/title where supported
        try:
            ico_path = RESOURCE_DIR.joinpath("assets", "icon.ico")
            if ico_path.exists():
                self.root.iconbitmap(str(ico_path))
        except Exception:
            pass
        self.title_icon.pack(side="left", padx=(8, 6))

        self.title_label = tk.Label(self.title_bar, text="Minimal To-Do", font=("Segoe UI", 10, "bold"), bg="#111111", fg="#ffffff")
        self.title_label.pack(side="left")

        self.title_controls = tk.Frame(self.title_bar, bg="#111111")
        self.title_controls.pack(side="right", padx=4)

        self.min_button = tk.Button(self.title_controls, text="—", command=self.root.iconify, bd=0, bg="#111111", fg="#ffffff", activeforeground="#ffffff")
        self.min_button.pack(side="right", padx=(6, 2))
        self.close_button = tk.Button(self.title_controls, text="✕", command=self.root.destroy, bd=0, bg="#111111", fg="#ffffff", activeforeground="#ffffff")
        self.close_button.pack(side="right")

        # hover bindings for nicer button UX
        self.min_button.bind("<Enter>", lambda e: self.min_button.configure(cursor="hand2"))
        self.min_button.bind("<Leave>", lambda e: self.min_button.configure(cursor=""))
        self.close_button.bind("<Enter>", lambda e: self.close_button.configure(cursor="hand2"))
        self.close_button.bind("<Leave>", lambda e: self.close_button.configure(cursor=""))

        # Content area
        self.content_frame = tk.Frame(root, bg="#ffffff", bd=0)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.subtitle_label = tk.Label(self.content_frame, text="A minimal black-and-white to-do.", font=("Segoe UI", 9), bg="#ffffff", fg="#444444")
        self.subtitle_label.pack(pady=(14, 6))

        self.input_frame = tk.Frame(self.content_frame, bg="#f5f5f5")
        self.input_frame.pack(fill="x", padx=20, pady=6)

        # use a tk.Entry so we can control background/foreground colours directly
        self.task_entry = tk.Entry(self.input_frame, font=("Segoe UI", 10))
        self.task_entry.pack(side="left", fill="x", expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = ttk.Button(self.input_frame, text="Add", command=self.add_task)
        self.add_button.pack(side="left", padx=(8, 0))

        self.theme_button = ttk.Button(self.input_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_button.pack(side="left", padx=(8, 0))

        self.list_frame = tk.Frame(self.content_frame, bg="#ffffff")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 16))

        self.listbox = tk.Listbox(
            self.list_frame,
            height=9,
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

        self.button_frame = tk.Frame(self.content_frame, bg="#ffffff")
        self.button_frame.pack(fill="x", padx=20, pady=(0, 18))

        self.delete_button = ttk.Button(self.button_frame, text="Delete", command=self.delete_task)
        self.delete_button.pack(side="left")
        self.delete_button.state(["disabled"])

        self.important_button = ttk.Button(self.button_frame, text="Mark Important", command=self.toggle_important)
        self.important_button.pack(side="left", padx=(8, 0))
        self.important_button.state(["disabled"])

        self.apply_theme()
        self.refresh_tasks()

        # make title bar draggable
        self._drag_data = {"x": 0, "y": 0}
        for w in (self.title_bar, self.title_label, self.title_icon):
            w.bind("<ButtonPress-1>", self._start_move)
            w.bind("<B1-Motion>", self._do_move)

        # ensure control buttons get theme updates as well
        self.min_button.configure(activebackground="#bbbbbb")
        self.close_button.configure(activebackground="#ff5555")

        # bind hover color behavior (methods set in apply_theme)
        self.min_button.bind("<Enter>", self._on_min_enter)
        self.min_button.bind("<Leave>", self._on_min_leave)
        self.close_button.bind("<Enter>", self._on_close_enter)
        self.close_button.bind("<Leave>", self._on_close_leave)

    def _start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _do_move(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")

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
            title_bg = "#181818"
            control_bg = "#181818"
        else:
            bg = "#ffffff"
            fg = "#111111"
            muted = "#666666"
            entry_bg = "#f5f5f5"
            entry_fg = "#111111"
            list_bg = "#ffffff"
            select_bg = "#000000"
            select_fg = "#ffffff"
            border = "#cccccc"
            title_bg = "#111111"
            control_bg = "#111111"

        self.root.configure(bg=bg)
        self.title_bar.configure(bg=title_bg)
        self.title_icon.configure(bg=title_bg, fg=fg)
        self.title_label.configure(bg=title_bg, fg="#ffffff")
        self.title_controls.configure(bg=control_bg)
        self.min_button.configure(bg=control_bg, fg="#ffffff", activebackground=border)
        self.close_button.configure(bg=control_bg, fg="#ffffff", activebackground="#ff5555")
        # hover colours
        self.theme_bg = bg
        self.btn_hover_bg = "#3a3a3a" if self.dark_mode else "#e6e6e6"
        self.close_hover_bg = "#b22222" if self.dark_mode else "#ff4444"
        self.content_frame.configure(bg="#ffffff" if not self.dark_mode else bg)
        self.subtitle_label.configure(bg="#ffffff" if not self.dark_mode else bg, fg=muted)
        self.input_frame.configure(bg="#f5f5f5" if not self.dark_mode else bg)
        self.list_frame.configure(bg="#ffffff" if not self.dark_mode else bg)
        self.button_frame.configure(bg="#ffffff" if not self.dark_mode else bg)

        self.task_entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        self.listbox.configure(bg=list_bg, fg=fg, selectbackground=select_bg, selectforeground=select_fg, highlightbackground=border, highlightcolor=border)

        style = ttk.Style()
        style.configure("TButton", foreground=fg, background=bg)
        style.map("TButton", background=[("active", "#3f3f3f" if self.dark_mode else "#e6e6e6")])
        self.theme_button.configure(text="Light Mode" if self.dark_mode else "Dark Mode")

    # hover handlers for title controls
    def _on_min_enter(self, _event):
        try:
            self.min_button.configure(bg=self.btn_hover_bg)
        except Exception:
            pass

    def _on_min_leave(self, _event):
        try:
            self.min_button.configure(bg=self.theme_bg)
        except Exception:
            pass

    def _on_close_enter(self, _event):
        try:
            self.close_button.configure(bg=self.close_hover_bg)
        except Exception:
            pass

    def _on_close_leave(self, _event):
        try:
            self.close_button.configure(bg=self.theme_bg)
        except Exception:
            pass

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
