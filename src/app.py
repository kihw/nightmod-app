from src.ui_setup import NightModUI
from src.monitoring import MonitoringManager
import tkinter as tk
from src.config import ConfigManager
from src.tray import TrayIcon

class NightModApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_all()

        self.ui = NightModUI(self, self.config)
        self.monitoring_manager = MonitoringManager(self, self.config, self.on_user_response, self.on_no_response)

        self.tray_icon = TrayIcon(
            self,
            self.ui.toggle_visibility,
            self.toggle_monitoring,
            self.on_close
        )
        self.tray_icon.setup()

        if self.config.get("start_with_system", False):
            self.toggle_monitoring()

    def toggle_monitoring(self):
        if self.monitoring_manager.is_running:
            self.monitoring_manager.stop_monitoring()
            self.ui.update_status("Inactif", active=False)
        else:
            self.monitoring_manager.start_monitoring()
            self.ui.update_status("Actif", active=True)

    def on_user_response(self):
        # Callback quand l'utilisateur répond au popup
        pass

    def on_no_response(self):
        # Callback quand l'utilisateur ne répond pas au popup
        self.monitoring_manager.stop_monitoring()

    def on_close(self):
        if self.monitoring_manager.is_running:
            if not self.ui.confirm_quit():
                return
            self.monitoring_manager.stop_monitoring()
        if self.tray_icon:
            self.tray_icon.stop()
        self.destroy()

if __name__ == "__main__":
    app = NightModApp()
    app.mainloop()
