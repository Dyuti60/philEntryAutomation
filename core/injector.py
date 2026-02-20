import json
from utils.logger import Logger


class Injector:

    def __init__(self, page):
        self.page = page
        self._routes = []

    # ============================
    # Internal Route Registration
    # ============================

    def _register_route(self, url_pattern, handler):
        Logger.info(f"Registering route interception -> {url_pattern}")
        self.page.route(url_pattern, handler)
        self._routes.append(url_pattern)

    # ============================
    # Modify Outgoing Request
    # ============================

    def modify_request(self, url_pattern, modifier_func):

        def handler(route, request):
            try:
                body = None
                if request.post_data:
                    try:
                        body = request.post_data_json()
                    except Exception:
                        body = request.post_data

                Logger.info(f"Original Request -> {request.url} | {body}")

                modified_body = modifier_func(body) if body else body

                Logger.info(f"Modified Request -> {modified_body}")

                route.continue_(
                    post_data=json.dumps(modified_body)
                    if isinstance(modified_body, dict)
                    else modified_body
                )

            except Exception as e:
                Logger.error("Request modification failed", e)
                route.continue_()

        self._register_route(url_pattern, handler)

    # ============================
    # Modify Incoming Response
    # ============================

    def modify_response(self, url_pattern, modifier_func):

        def handler(route, request):
            try:
                response = route.fetch()

                try:
                    body = response.json()
                except Exception:
                    body = response.text()

                Logger.info(f"Original Response -> {request.url} | {body}")

                modified_body = modifier_func(body)

                Logger.info(f"Modified Response -> {modified_body}")

                route.fulfill(
                    response=response,
                    json=modified_body
                    if isinstance(modified_body, dict)
                    else None,
                    body=json.dumps(modified_body)
                    if not isinstance(modified_body, dict)
                    else None
                )

            except Exception as e:
                Logger.error("Response modification failed", e)
                route.continue_()

        self._register_route(url_pattern, handler)

    # ============================
    # Full API Mock
    # ============================

    def mock_api(self, url_pattern, mock_body, status=200):

        def handler(route, request):
            Logger.info(f"Mocking API -> {request.url}")

            route.fulfill(
                status=status,
                content_type="application/json",
                body=json.dumps(mock_body)
            )

        self._register_route(url_pattern, handler)

    # ============================
    # Abort Request
    # ============================

    def abort_request(self, url_pattern):

        def handler(route, request):
            Logger.warn(f"Aborting request -> {request.url}")
            route.abort()

        self._register_route(url_pattern, handler)

    # ============================
    # Add Header Injection
    # ============================

    def add_header(self, url_pattern, headers: dict):

        def handler(route, request):
            updated_headers = request.headers.copy()
            updated_headers.update(headers)

            Logger.info(f"Injecting headers -> {headers}")

            route.continue_(headers=updated_headers)

        self._register_route(url_pattern, handler)

    # ============================
    # Cleanup
    # ============================

    def clear_routes(self):
        for pattern in self._routes:
            try:
                self.page.unroute(pattern)
            except Exception:
                pass

        self._routes.clear()
        Logger.info("Cleared all injection routes")
