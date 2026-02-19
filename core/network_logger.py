import json
from utils.logger import Logger


class NetworkLogger:

    def __init__(self, page):
        self.page = page
        self.logs = []
        self.server_errors = []

    def start(self):

        def on_request(request):
            entry = {
                "type": "REQUEST",
                "method": request.method,
                "url": request.url,
            }

            try:
                entry["payload"] = request.post_data_json()
            except Exception:
                entry["payload"] = request.post_data

            self.logs.append(entry)

            Logger.info(f"REQUEST → {request.method} {request.url}")

        def on_response(response):
            entry = {
                "type": "RESPONSE",
                "url": response.url,
                "status": response.status,
            }

            try:
                entry["body"] = response.json()
            except Exception:
                entry["body"] = response.text()

            self.logs.append(entry)

            Logger.info(f"RESPONSE ← {response.status} {response.url}")

            # Log error responses
            if response.status >= 400:
                Logger.error(f"Network Error {response.status} → {response.url}")

            if response.status>=500:
                self.server_errors.append(entry)

        self.page.on("request", on_request)
        self.page.on("response", on_response)

    def has_server_error(self):
        return len(self.server_errors)>0

    def get_logs(self):
        return self.logs

    def clear(self):
        self.logs.clear()
