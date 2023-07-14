import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import psutil

class TaskManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.root.geometry("600x400")

        # Load background image
        self.background_image = Image.open("dummy.jpeg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.process_table = ttk.Treeview(self.root, columns=("pid", "name", "memory"), show="headings")
        self.process_table.heading("pid", text="PID")
        self.process_table.heading("name", text="Name")
        self.process_table.heading("memory", text="Memory Usage")
        self.process_table.column("pid", width=100, anchor="center")
        self.process_table.column("name", width=200, anchor="w")
        self.process_table.column("memory", width=200, anchor="center")
        self.process_table.pack(fill=tk.BOTH, expand=True)

        self.kill_button = tk.Button(self.root, text="Kill", command=self.kill_selected_processes)
        self.kill_button.pack(pady=10)

        self.update_process_list()

    def kill_selected_processes(self):
        selected_items = self.process_table.selection()
        if len(selected_items) == 0:
            messagebox.showinfo("Kill Processes", "No processes selected.")
            return

        process_list = []
        for item in selected_items:
            process_info = self.process_table.item(item)
            process_pid = process_info["values"][0]
            process_list.append(int(process_pid))

        for pid in process_list:
            try:
                process = psutil.Process(pid)
                process.terminate()
            except psutil.NoSuchProcess:
                pass

        messagebox.showinfo("Kill Processes", "Selected processes have been terminated.")
        self.update_process_list()

    def update_process_list(self):
        self.process_table.delete(*self.process_table.get_children())

        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            pid = proc.info['pid']
            name = proc.info['name']
            memory = proc.info['memory_info'].rss / 1024 / 1024  # Convert to MB
            self.process_table.insert("", tk.END, values=(pid, name, f"{memory:.2f} MB"))

        self.root.after(2000, self.update_process_list)

    def run(self):
        self.root.mainloop()

app = TaskManagerApp()
app.run()
