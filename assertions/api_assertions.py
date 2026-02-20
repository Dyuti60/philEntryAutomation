import allure
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from utils.logger import Logger


class APIAssert:

    # ============================
    # Status Code Assertion
    # ============================

    @staticmethod
    @allure.step("Verify status code equals {expected}")
    def status_code(actual: int, expected: int, message: str = None):
        assert actual == expected, message or f"Expected {expected}, got {actual}"
        Logger.info(f"API ASSERT -> Status code matched: {expected}")

    # ============================
    # Key Exists
    # ============================

    @staticmethod
    @allure.step('Verify response has key "{key}"')
    def has_key(response_body: dict, key: str, message: str = None):
        assert key in response_body, message or f"Missing key: {key}"
        Logger.info(f"API ASSERT -> Key exists: {key}")

    # ============================
    # Value Equals
    # ============================

    @staticmethod
    @allure.step("Verify value equals expected")
    def value_equals(actual, expected, message: str = None):
        assert actual == expected, message or f"Expected {expected}, got {actual}"
        Logger.info("API ASSERT -> Value matched")

    # ============================
    # Array Not Empty
    # ============================

    @staticmethod
    @allure.step("Verify array is not empty")
    def array_not_empty(array: list, message: str = None):
        assert isinstance(array, list), "Provided object is not a list"
        assert len(array) > 0, message or "Array is empty"
        Logger.info("API ASSERT -> Array not empty")

    # ============================
    # Full JSON Equals
    # ============================

    @staticmethod
    @allure.step("Verify full JSON equals expected")
    def json_equals(actual: dict, expected: dict, message: str = None):
        assert actual == expected, message or "JSON mismatch"
        Logger.info("API ASSERT -> JSON matched completely")

    # ============================
    # JSON Schema Validation
    # ============================

    @staticmethod
    @allure.step("Validate response against JSON schema")
    def validate_schema(response_body: dict, schema: dict):
        try:
            validate(instance=response_body, schema=schema)
            Logger.info("API ASSERT -> Schema validation passed")
        except ValidationError as e:
            Logger.error("Schema validation failed", e)
            raise AssertionError(f"Schema validation failed: {e.message}")
