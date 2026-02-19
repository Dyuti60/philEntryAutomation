from playwright.sync_api import Page
from utils.logger import Logger
import time
import allure

class MouseManager:

    def __init__(self, page: Page):
        self.page = page

    # =============================
    # Retry Wrapper (Optional Safety)
    # =============================

    def _retry(self, action, retries=3, delay=0.5):
        for i in range(retries):
            try:
                action()
                return
            except Exception as e:
                if i == retries - 1:
                    raise e
                Logger.warn(f"Retrying mouse action ({i+1}/{retries})")
                time.sleep(delay)

    # =============================
    # Hover
    # =============================

    def hover(self, locator: str):
        def action():
            step_name = f"Mouse -> Hover: "
            with allure.step(step_name):
                Logger.info(f"MOUSE → Hover: {locator}")
                element = self.page.locator(locator)
                element.wait_for(state="visible")
                element.hover()

        self._retry(action)

    # =============================
    # Right Click
    # =============================

    def right_click(self, locator: str):
        def action():
            step_name = f"Mouse -> Right click: "
            with allure.step(step_name):
                Logger.info(f"MOUSE → Right click: {locator}")
                element = self.page.locator(locator)
                element.wait_for(state="visible")
                element.click(button="right")

        self._retry(action)

    # =============================
    # Double Click
    # =============================

    def double_click(self, locator: str):
        def action():
            step_name = f"MOUSE → Double click: {locator}"
            with allure.step(step_name):
                Logger.info(f"MOUSE → Double click: {locator}")
                element = self.page.locator(locator)
                element.wait_for(state="visible")
                element.dblclick()

        self._retry(action)

    # =============================
    # Drag and Drop
    # =============================

    def drag_and_drop(self, source: str, target: str):
        def action():
            step_name = f"MOUSE → Drag {source} → {target}"
            with allure.step(step_name):
                Logger.info(f"MOUSE → Drag {source} → {target}")

                source_el = self.page.locator(source)
                target_el = self.page.locator(target)

                source_el.wait_for(state="visible")
                target_el.wait_for(state="visible")

                self.page.drag_and_drop(source, target)

        self._retry(action)
