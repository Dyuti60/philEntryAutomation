import platform
from playwright.sync_api import Page
from utils.logger import Logger


class KeyboardManager:

    def __init__(self, page: Page):
        self.page = page

        # Detect OS for correct modifier key
        self.is_mac = platform.system() == "Darwin"
        self.modifier = "Meta" if self.is_mac else "Control"

    # =============================
    # Basic Key Presses
    # =============================

    def press_enter(self):
        Logger.info("KEYBOARD → Press ENTER")
        self.page.keyboard.press("Enter")

    def press_tab(self):
        Logger.info("KEYBOARD → Press TAB")
        self.page.keyboard.press("Tab")

    def press_escape(self):
        Logger.info("KEYBOARD → Press ESCAPE")
        self.page.keyboard.press("Escape")

    # =============================
    # Shortcut Keys
    # =============================

    def select_all(self):
        Logger.info("KEYBOARD → Select All")
        self.page.keyboard.press(f"{self.modifier}+A")

    def copy(self):
        Logger.info("KEYBOARD → Copy")
        self.page.keyboard.press(f"{self.modifier}+C")

    def paste(self):
        Logger.info("KEYBOARD → Paste")
        self.page.keyboard.press(f"{self.modifier}+V")

    # =============================
    # Typing
    # =============================

    def type_text(self, text: str, delay: float = 0):
        Logger.info(f"KEYBOARD → Type text: {text}")
        self.page.keyboard.type(text, delay=delay)
