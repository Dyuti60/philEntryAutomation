from playwright.sync_api import Page
from utils.logger import Logger
import time


class WaitManager:

    def __init__(self, page: Page):
        self.page = page

    # =============================
    # Wait for Network Idle
    # =============================

    def for_network_idle(self, timeout: int = 5000):
        Logger.info("WAIT → Network idle")
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    # # =============================
    # # Wait for DOM Stable
    # # =============================

    # def for_dom_stable(self, timeout: int = 5000):
    #     Logger.info("WAIT → DOM stable")

    #     # Wait for DOM to stop changing
    #     self.page.wait_for_function(
    #         """
    #         () => {
    #             return new Promise(resolve => {
    #                 let timer;
    #                 const observer = new MutationObserver(() => {
    #                     clearTimeout(timer);
    #                     timer = setTimeout(() => {
    #                         observer.disconnect();
    #                         resolve(true);
    #                     }, 500);
    #                 });

    #                 observer.observe(document.body, {
    #                     childList: true,
    #                     subtree: true
    #                 });

    #                 timer = setTimeout(() => {
    #                     observer.disconnect();
    #                     resolve(true);
    #                 }, 500);
    #             });
    #         }
    #         """,
    #         timeout=timeout
    #     )

    # =============================
    # Wait for Visible
    # =============================

    def wait_for_visible(self, locator: str, timeout: int = 5000):
        Logger.info(f"WAIT → Visible: {locator}")
        self.page.wait_for_selector(locator, state="visible", timeout=timeout)

    # =============================
    # Wait for Hidden
    # =============================

    def wait_for_hidden(self, locator: str, timeout: int = 5000):
        Logger.info(f"WAIT → Hidden: {locator}")
        self.page.wait_for_selector(locator, state="hidden", timeout=timeout)

    # =============================
    # Wait for Attached
    # =============================

    def wait_for_attached(self, locator: str, timeout: int = 5000):
        Logger.info(f"WAIT → Attached: {locator}")
        self.page.wait_for_selector(locator, state="attached", timeout=timeout)

    # =============================
    # Hard Timeout
    # =============================

    def wait_for_timeout(self, ms: int):
        Logger.info(f"WAIT → Timeout: {ms}ms")
        self.page.wait_for_timeout(ms)

    # =============================
    # Wait Until Condition True
    # =============================

    def wait_until(self, condition_func, timeout=5000, interval=0.5):
        Logger.info("WAIT → Custom condition")

        end_time = time.time() + timeout / 1000

        while time.time() < end_time:
            if condition_func():
                return True
            time.sleep(interval)

        raise TimeoutError("Custom wait condition timed out")
