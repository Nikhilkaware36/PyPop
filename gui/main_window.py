import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading, time, subprocess, pkg_resources, itertools, requests, webbrowser
from core.shell_runner import install_library_shell

# --- Animated Text Function ---
def animate_status(label, text, delay=0.05):
    label.config(text="")
    def animate():
        displayed = ""
        for char in text:
            displayed += char
            label.config(text=displayed)
            label.update()
            time.sleep(delay)
    threading.Thread(target=animate).start()

# Spinner animation
class Spinner:
    def __init__(self, label):
        self.label = label
        self.running = False
        self.spinner = itertools.cycle(['⠋', '⠙', '⠸', '⠴', '⠦', '⠇'])

    def start(self):
        self.running = True
        threading.Thread(target=self.update).start()

    def stop(self):
        self.running = False
        self.label.config(text="Installation Complete ✅")

    def update(self):
        while self.running:
            spin = next(self.spinner)
            self.label.config(text=f"Installing... {spin}")
            time.sleep(0.2)

ALL_PYPI_LIBRARIES = ["numpy", "pandas", "requests", "flask", "matplotlib", "scikit-learn", "torch", "tensorflow"]
INSTALLED_LIBRARIES = {pkg.key for pkg in pkg_resources.working_set}

def get_uninstalled_libraries():
    return [lib for lib in ALL_PYPI_LIBRARIES if lib not in INSTALLED_LIBRARIES]

def is_library_valid(lib):
    try:
        response = requests.get(f"https://pypi.org/pypi/{lib}/json")
        return response.status_code == 200
    except:
        return False

def is_installed(lib):
    return lib.lower() in {pkg.key for pkg in pkg_resources.working_set}

def launch_gui():
    root = tk.Tk()
    root.title("🔥 PyPop – Bash-Based Python Library Installer")
    root.geometry("580x640")
    root.configure(bg="#121212")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#121212')
    style.configure('TLabel', background='#121212', foreground='#ffffff', font=('JetBrains Mono', 10))
    style.configure('TEntry', fieldbackground='#2a2a2a', foreground='white')
    style.configure('TButton', background='#ff4081', foreground='white', font=('JetBrains Mono', 10, 'bold'))
    style.map('TButton', background=[('active', '#e91e63')])
    style.configure('TRadiobutton', background='#121212', foreground='white')

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill='both', expand=True)

    title_label = ttk.Label(main_frame, text="🔥 PyPop – Python Library Installer", font=('JetBrains Mono', 12, 'bold'))
    title_label.pack(pady=(0, 15))

    mode_var = tk.StringVar(value="manual")

    def update_mode():
        if mode_var.get() == "manual":
            lib_entry.configure(state='normal')
            install_btn.configure(state='disabled')
        else:
            lib_entry_var.set("")
            lib_entry.configure(state='disabled')
            install_btn.configure(state='normal')
        update_button_state()

    def update_button_state(*args):
        if mode_var.get() == "manual":
            install_btn.configure(state='normal' if lib_entry_var.get().strip() else 'disabled')

    ttk.Label(main_frame, text="Mode:").pack(anchor='w')
    ttk.Radiobutton(main_frame, text="Manual Mode", variable=mode_var, value="manual", command=update_mode).pack(anchor='w')
    ttk.Radiobutton(main_frame, text="Auto Mode (Install Missing Only)", variable=mode_var, value="auto", command=update_mode).pack(anchor='w')

    ttk.Label(main_frame, text="\nEnter Library (Manual Only):").pack(anchor='w')
    lib_entry_var = tk.StringVar()
    lib_entry_var.trace_add("write", update_button_state)
    lib_entry = ttk.Entry(main_frame, width=40, textvariable=lib_entry_var)
    lib_entry.pack(pady=5)

    suggestion_label = ttk.Label(main_frame, text="Tip: Type a correct pip library name", font=('JetBrains Mono', 9), foreground="#ffaa00")
    suggestion_label.pack(pady=(0, 10))

    progress = ttk.Progressbar(main_frame, length=420, mode='determinate')
    progress.pack(pady=(10, 5))
    status_label = ttk.Label(main_frame, text="Ready", font=('JetBrains Mono', 9, 'italic'), foreground="#aaaaaa")
    status_label.pack()
    spinner = Spinner(status_label)

    output_box = scrolledtext.ScrolledText(main_frame, width=65, height=12, wrap='word', bg='#1e1e1e', fg='#00ffcc')
    output_box.pack(pady=10)

    def install_library():
        if mode_var.get() == "manual":
            library = lib_entry_var.get().strip()
            if not library:
                messagebox.showwarning("Input Error", "Please enter a library name.")
                return
            if not is_library_valid(library):
                messagebox.showerror("Invalid Library", f"The library '{library}' does not exist on PyPI.")
                return
            libraries_to_install = [library]
        else:
            libraries_to_install = get_uninstalled_libraries()
            if not libraries_to_install:
                messagebox.showinfo("No Missing Packages", "All major libraries are already installed.")
                return
            est_size = round(len(libraries_to_install) * 0.03, 2)
            confirm = messagebox.askyesno("Auto Install", f"{len(libraries_to_install)} libraries missing.\nEstimated size: {est_size} GB.\nInstall now?")
            if not confirm:
                return

        animate_status(status_label, f"Installing {len(libraries_to_install)} libraries...")
        progress['value'] = 0
        spinner.start()
        output_box.delete(1.0, tk.END)

        def run_install():
            step = 100 // max(1, len(libraries_to_install))
            output = ""
            for idx, lib in enumerate(libraries_to_install):
                if is_installed(lib):
                    msg = f"✅ Already installed: {lib}\n"
                    output += msg
                    output_box.insert(tk.END, msg)
                    continue
                msg = f"🔄 Installing: {lib}\n"
                output += msg
                output_box.insert(tk.END, msg)
                try:
                    result = subprocess.run(["pip", "install", lib], capture_output=True, text=True)
                    output += result.stdout + result.stderr
                    output_box.insert(tk.END, result.stdout)
                    output_box.insert(tk.END, result.stderr)
                except Exception as e:
                    error_msg = f"Error: {str(e)}\n"
                    output += error_msg
                    output_box.insert(tk.END, error_msg)
                output_box.see(tk.END)
                progress['value'] = (idx + 1) * step
                root.update_idletasks()
                time.sleep(0.2)
            spinner.stop()

            from datetime import datetime
            log_dir = os.path.expanduser("~/.pypop/logs")
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = os.path.join(log_dir, f"install_{timestamp}.txt")
            with open(log_file, "w") as f:
                f.write(output)

            messagebox.showinfo("Done", f"Installation completed. Log saved to {log_file}")

        threading.Thread(target=run_install).start()

    install_btn = ttk.Button(main_frame, text="🚀 Start Installation", command=install_library)
    install_btn.pack(pady=(15, 10))
    install_btn.configure(state='disabled')

    # GitHub Credit Label
    def open_github(event=None):
        webbrowser.open_new("https://github.com/Nikhilkaware36")

    footer = ttk.Label(
        main_frame,
        text="Created by Nikhil Kaware · GitHub: @Nikhilkaware36",
        font=('JetBrains Mono', 9, 'italic'),
        foreground="#6666ff",
        cursor="hand2"
    )
    footer.pack(pady=(10, 0))
    footer.bind("<Button-1>", open_github)

    update_mode()
    root.mainloop()

