import tkinter as tk
from tkinter import ttk, messagebox
import os
import platform
import logging

logger = logging.getLogger("NightMod.UI")

class NightModUI:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        
        self.status_var = tk.StringVar(value="Inactif")
        self.next_check_var = tk.StringVar(value="Aucune vérification prévue")

        self.setup_main_window()
        self.setup_ui()

    def setup_main_window(self):
        self.root.title("NightMod")
        self.root.geometry("480x520")
        self.root.minsize(480, 520)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 480) // 2
        y = (screen_height - 520) // 2
        self.root.geometry(f"+{x}+{y}")

        self.configure_theme()
        self.set_application_icon()

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.toggle_visibility())

        self.root.bind("<Alt-q>", lambda e: self.root.quit())
        self.root.bind("<Alt-n>", lambda e: self.toggle_visibility())

    def configure_theme(self):
        try:
            self.root.configure(bg="#1a1a1a")
            self.style = ttk.Style(self.root)
            self.style.configure("TLabel", background="#1a1a1a", foreground="#FFFFFF")
            self.style.configure("TButton", background="#2d2d2d", foreground="#FFFFFF")
            logger.info("Thème appliqué avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'application du thème: {e}")

    def set_application_icon(self):
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icon.png")
            if platform.system() == "Windows":
                ico_path = icon_path.replace(".png", ".ico")
                if os.path.exists(ico_path):
                    self.root.iconbitmap(ico_path)
            elif os.path.exists(icon_path):
                from PIL import Image, ImageTk
                img = Image.open(icon_path).resize((64, 64))
                icon = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, icon)
        except Exception as e:
            logger.warning(f"Impossible de charger l'icône: {e}")

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="30 35 30 35")
        main_frame.pack(fill=tk.BOTH, expand=True)

        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 20))

        self.status_indicator = ttk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 14),
            foreground="#888888"
        )
        self.status_indicator.grid(row=0, column=0, padx=(0, 15))

        ttk.Label(status_frame, text="État").grid(row=0, column=1, sticky=tk.W)
        ttk.Label(status_frame, textvariable=self.status_var).grid(row=0, column=2, sticky=tk.W, padx=10)

    def update_status(self, status, active=False):
        self.status_var.set(status)
        self.status_indicator.config(foreground="#4CAF50" if active else "#888888")

    def toggle_visibility(self):
        if self.root.state() == 'withdrawn':
            self.root.deiconify()
            self.root.lift()
        else:
            self.root.withdraw()

    def confirm_quit(self):
        return messagebox.askyesno("NightMod", "La surveillance est en cours. Voulez-vous vraiment quitter NightMod ?")
