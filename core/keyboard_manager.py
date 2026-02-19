import platform
from playwright.sync_api import Page
from utils.logger import Logger
import allure

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
        step_name = f"KEYBOARD → Press ENTER "
        with allure.step(step_name):
            Logger.info("KEYBOARD → Press ENTER")
            self.page.keyboard.press("Enter")

    def press_tab(self):
        step_name = f"KEYBOARD → Press TAB "
        with allure.step(step_name):
            Logger.info("KEYBOARD → Press TAB")
            self.page.keyboard.press("Tab")

    def press_escape(self):
        step_name = f"KEYBOARD → Press ESCAPE"
        with allure.step(step_name):
            Logger.info("KEYBOARD → Press ESCAPE")
            self.page.keyboard.press("Escape")

    # =============================
    # Shortcut Keys
    # =============================

    def select_all(self):
        step_name = f"KEYBOARD → Select All "
        with allure.step(step_name):
            Logger.info("KEYBOARD → Select All")
            self.page.keyboard.press(f"{self.modifier}+A")

    def copy(self):
        step_name = f"KEYBOARD → Copy "
        with allure.step(step_name):
            Logger.info("KEYBOARD → Copy")
            self.page.keyboard.press(f"{self.modifier}+C")

    def paste(self):
        step_name = f"KEYBOARD → Paste "
        with allure.step(step_name):
            Logger.info("KEYBOARD → Paste")
            self.page.keyboard.press(f"{self.modifier}+V")

    # =============================
    # Typing
    # =============================

    def type_text(self, text: str, delay: float = 0):
        step_name = f"KEYBOARD → Type text: {text}"
        with allure.step(step_name):
            Logger.info(f"KEYBOARD → Type text: {text}")
            self.page.keyboard.type(text, delay=delay)
