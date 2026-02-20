import time
from typing import List
from playwright.sync_api import Page, Locator, ElementHandle
from utils.logger import Logger
import allure

class ActionManager:

    def __init__(self, page: Page):
        self.page = page

    # =============================
    # Retry Mechanism
    # =============================

    def _retry(self, action, retries=1, delay=0.5):
        for i in range(retries):
            try:
                action()
                return
            except Exception as e:
                if i == retries - 1:
                    raise e
                Logger.warn(f"Retrying action ({i+1}/{retries})")
                time.sleep(delay)

    # =============================
    # Navigation
    # =============================

    def goto(self, url: str):
        step_name = f"ACTION -> Navigate to: {url}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Navigate to: {url}")
            self.page.goto(url, wait_until="domcontentloaded")

    # =============================
    # Click Actions
    # =============================

    def click(self, locator: str):
        def action():
            step_name = f"ACTION -> Click: {locator}"
            with allure.step(step_name):
                Logger.info(f"ACTION -> Click: {locator}")
                element = self.page.locator(locator)
                element.wait_for(state="visible")
                element.scroll_into_view_if_needed()
                self.page.wait_for_timeout(200)
                element.click(timeout=5000)

        self._retry(action)

    def click_first(self, locator: str):
        def action():
            step_name = f"ACTION -> Click first: {locator}"
            with allure.step(step_name):
                Logger.info(f"ACTION -> Click first: {locator}")
                element = self.page.locator(locator)
                element.wait_for(state="visible")
                element.first.click(timeout=5000)

        self._retry(action)

    def click_last(self, locator: str):
        def action():
            step_name = f"ACTION -> Click last: {locator}"
            with allure.step(step_name):
                Logger.info(f"ACTION -> Click last: {locator}")
                element = self.page.locator(locator)
                element.wait_for(state="visible")
                element.last.click(timeout=5000)

        self._retry(action)

    # =============================
    # Text-based Click
    # =============================

    def click_option_by_text(self, text: str):
        def action():
            step_name = f"ACTION -> Click option by text: {text}"
            with allure.step(step_name):
                Logger.info(f"ACTION -> Click option by text: {text}")
                self.page.wait_for_selector(f"text=/{text}/i")
                self.page.locator(f"text=/{text}/i").click(timeout=5000)

        self._retry(action)

    # =============================
    # Type Actions
    # =============================

    def type(self, locator: str, text: str):
        def action():
            step_name = f"ACTION -> Type into: {locator}"
            with allure.step(step_name):
                Logger.info(f"ACTION -> Type into: {locator}")
                self.page.wait_for_selector(locator)
                self.page.fill(locator, text)

        self._retry(action)

    def clear_and_type(self, locator: str, text: str):
        def action():
            step_name = f"ACTION -> Clear & type: {locator}"
            with allure.step(step_name):
                Logger.info(f"ACTION -> Clear & Type: {locator}")
                self.page.fill(locator, "")
                self.page.type(locator, text)

        self._retry(action)

    # =============================
    # Scroll Actions
    # =============================

    def scroll_down(self, pixels=500):
        step_name = f"ACTION -> Scroll down by {pixels}px"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Scroll down {pixels}px")
            self.page.evaluate("(y) => window.scrollBy(0, y)", pixels)

    def scroll_up(self, pixels=500):
        step_name = f"ACTION -> Scroll up by {pixels}px"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Scroll up {pixels}px")
            self.page.evaluate("(y) => window.scrollBy(0, -y)", pixels)

    def scroll_into_view(self, locator: str):
        step_name = f"ACTION -> Scroll into view: {locator}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Scroll into view: {locator}")
            self.page.locator(locator).scroll_into_view_if_needed()

    # =============================
    # Scroll Until Text Visible
    # =============================

    def scroll_till_text_visible(
        self, locator: str, expected_text: str,
        max_scrolls=10, scroll_pixels=400
    ) -> bool:
        step_name = f"ACTION -> Scroll till text visible: {expected_text}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Scroll till text visible: {expected_text}")

            for i in range(max_scrolls):
                texts = self.get_texts(locator)

                if any(expected_text.lower() in t.lower() for t in texts):
                    Logger.info(f"Text found after {i+1} scroll(s)")
                    return True

                self.scroll_down(scroll_pixels)
                self.page.wait_for_timeout(500)

            Logger.warn(f"Text not found: {expected_text}")
            return False

    # =============================
    # Getters
    # =============================

    def get_element(self, locator: str) -> Locator:
        step_name = f"ACTION -> Get element: {locator}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Get element: {locator}")
            self.page.wait_for_selector(locator)
            return self.page.locator(locator)

    def get_elements(self, locator: str) -> List[Locator]:
        step_name = f"ACTION -> Get elements list: {locator}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Get elements list: {locator}")
            self.page.wait_for_selector(locator)
            return self.page.locator(locator).all()

    def get_text(self, locator: str) -> str:
        step_name = f"ACTION -> Get text: {locator}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Get text: {locator}")
            self.page.wait_for_selector(locator)
            return (self.page.text_content(locator) or "").strip()

    def get_texts(self, locator: str) -> List[str]:
        step_name = f"ACTION -> Get texts list: {locator}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Get texts list: {locator}")
            self.page.wait_for_selector(locator)
            return self.page.eval_on_selector_all(
                locator,
                "els => els.map(e => e.textContent?.trim() || '')"
            )

    def get_input_value(self, locator: str) -> str:
        step_name = f"ACTION -> Get input value: {locator}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Get input value: {locator}")
            self.page.wait_for_selector(locator)
            return (self.page.input_value(locator) or "").strip()

    def get_attribute(self, locator: str, attribute: str):
        step_name = f"ACTION -> Get attribute {attribute} from {locator}"
        with allure.step(step_name):
            Logger.info(f"ACTION -> Get attribute {attribute} from {locator}")
            self.page.wait_for_selector(locator)
            return self.page.get_attribute(locator, attribute)

    # =============================
    # State Checks
    # =============================

    def is_visible(self, locator: str) -> bool:
        try:
            return self.page.is_visible(locator)
        except Exception:
            return False

    def is_enabled(self, locator: str) -> bool:
        try:
            return self.page.is_enabled(locator)
        except Exception:
            return False

    def is_present(self, locator: str) -> bool:
        try:
            return self.page.query_selector(locator) is not None
        except Exception:
            return False
