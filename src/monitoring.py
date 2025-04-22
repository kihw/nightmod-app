import threading
import time
from datetime import datetime
from src.popup import PopupChecker
from src.system_actions import SystemActions
import logging

logger = logging.getLogger("NightMod.Monitoring")

class MonitoringManager:
    def __init__(self, root, config, on_user_response, on_no_response):
        self.root = root
        self.config = config
        self.on_user_response = on_user_response
        self.on_no_response = on_no_response

        self.is_running = False
        self.next_check_time = None
        self.timer_thread = None

    def start_monitoring(self):
        if self.is_running:
            return
        self.is_running = True
        self.timer_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.timer_thread.start()
        logger.info("Surveillance démarrée")

    def stop_monitoring(self):
        self.is_running = False
        self.next_check_time = None
        logger.info("Surveillance arrêtée")

    def monitoring_loop(self):
        while self.is_running:
            interval_seconds = self.config.get("check_interval_minutes", 20) * 60
            self.next_check_time = datetime.now().timestamp() + interval_seconds

            for _ in range(interval_seconds):
                if not self.is_running:
                    break
                time.sleep(1)

            if not self.is_running:
                break

            self.root.after(0, self.show_check_popup)

    def show_check_popup(self):
        response_time = self.config.get("response_time_seconds", 30)
        PopupChecker(
            self.root,
            response_time,
            self.on_user_response_callback,
            self.on_no_response_callback,
            self.config
        )

    def on_user_response_callback(self):
        logger.info("L'utilisateur a répondu au popup.")
        if self.on_user_response:
            self.on_user_response()

    def on_no_response_callback(self):
        logger.info("Aucune réponse détectée. Exécution de l'action configurée.")
        action = self.config.get("shutdown_action", "shutdown")
        try:
            SystemActions.perform_action(action)
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de l'action: {e}")
        if self.on_no_response:
            self.on_no_response()
