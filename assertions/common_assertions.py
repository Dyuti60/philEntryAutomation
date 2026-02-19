import allure
from utils.logger import Logger


class CommonAssert:

    # ============================
    # Is True
    # ============================

    @staticmethod
    @allure.step("Verify condition is TRUE")
    def is_true(condition: bool, message: str = None):
        assert condition is True, message or "Condition is False"
        Logger.info("GENERIC ASSERT → Condition is True")

    # ============================
    # Is False
    # ============================

    @staticmethod
    @allure.step("Verify condition is FALSE")
    def is_false(condition: bool, message: str = None):
        assert condition is False, message or "Condition is True"
        Logger.info("GENERIC ASSERT → Condition is False")

    # ============================
    # Is Not Null
    # ============================

    @staticmethod
    @allure.step("Verify value is NOT NULL")
    def is_not_null(value, message: str = None):
        assert value is not None, message or "Value is None"
        Logger.info("GENERIC ASSERT → Value is not null")

    # ============================
    # Is Defined (Python equivalent)
    # ============================

    @staticmethod
    @allure.step("Verify value is defined")
    def is_defined(value, message: str = None):
        assert value is not None, message or "Value is undefined"
        Logger.info("GENERIC ASSERT → Value is defined")

    # ============================
    # Equals
    # ============================

    @staticmethod
    @allure.step("Verify values are equal")
    def equals(actual, expected, message: str = None):
        assert actual == expected, message or \
            f"Expected '{expected}', got '{actual}'"

        Logger.info("GENERIC ASSERT → Values matched")
