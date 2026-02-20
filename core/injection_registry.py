from core.injector import Injector
from utils.logger import Logger


class InjectionRegistry:

    def __init__(self, page):
        self.injector = Injector(page)

    # ============================
    # Admin Login Profile
    # ============================

    def admin_profile(self):
        Logger.info("Applying Admin Profile")

        def modify(body):
            if body and isinstance(body, dict):
                body["role"] = "admin"
            return body

        self.injector.modify_request("**/login", modify)

    # ============================
    # Mock Payment API
    # ============================

    def mock_payment_profile(self):
        Logger.info("Applying Payment Mock Profile")

        self.injector.mock_api(
            "**/payment",
            {"status": "SUCCESS", "transactionId": "MOCK123"}
        )

    # ============================
    # Force Server Error
    # ============================

    def force_server_error_profile(self):
        Logger.info("Applying Forced 500 Error Profile")

        self.injector.mock_api(
            "**/api/**",
            {"error": "Internal Server Error"},
            status=500
        )

    # ============================
    # Disable Analytics
    # ============================

    def disable_analytics_profile(self):
        Logger.info("Disabling Analytics APIs")

        self.injector.abort_request("**/analytics/**")

    # ============================
    # Apply by Name
    # ============================

    def apply(self, profile_name: str):
        if hasattr(self, profile_name):
            Logger.info(f"Applying Injection Profile -> {profile_name}")
            getattr(self, profile_name)()
        else:
            Logger.warn(f"Injection profile not found -> {profile_name}")
