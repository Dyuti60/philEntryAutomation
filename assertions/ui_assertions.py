import allure
from utils.logger import Logger


class UIAssert:

    def __init__(self, page):
        self.page = page

    # ============================
    # Title Equals
    # ============================

    @allure.step('Verify page title equals "{expected_title}"')
    def title_equals(self, expected_title: str, message: str = None):
        actual_title = self.page.title()
        assert actual_title == expected_title, message or \
            f"Expected title '{expected_title}', got '{actual_title}'"

        Logger.info(f"UI ASSERT -> Title matched: {expected_title}")

    # ============================
    # URL Contains
    # ============================

    @allure.step('Verify URL contains "{partial_url}"')
    def url_contains(self, partial_url: str, message: str = None):
        current_url = self.page.url
        assert partial_url in current_url, message or \
            f"URL '{current_url}' does not contain '{partial_url}'"

        Logger.info(f"UI ASSERT -> URL contains: {partial_url}")

    # ============================
    # Element Visible
    # ============================

    @allure.step('Verify element visible: {locator}')
    def element_visible(self, locator: str, message: str = None):
        visible = self.page.is_visible(locator)
        assert visible, message or f"Element not visible: {locator}"

        Logger.info(f"UI ASSERT -> Element visible: {locator}")

    # ============================
    # Text Equals
    # ============================

    @allure.step('Verify text equals "{expected_text}"')
    def text_equals(self, locator: str, expected_text: str, message: str = None):
        actual_text = self.page.text_content(locator)
        actual_text = actual_text.strip() if actual_text else ""

        assert actual_text == expected_text, message or \
            f"Expected '{expected_text}', got '{actual_text}'"

        Logger.info(f"UI ASSERT -> Text matched: {expected_text}")

    # ============================
    # Text Contains
    # ============================

    @allure.step('Verify text contains "{expected_text}"')
    def text_contains(self, locator: str, expected_text: str, message: str = None):
        actual_text = self.page.text_content(locator) or ""

        assert expected_text in actual_text, message or \
            f"Text does not contain '{expected_text}'"

        Logger.info(f"UI ASSERT -> Text contains: {expected_text}")
