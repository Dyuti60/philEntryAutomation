from config.settings import settings
from utils.logger import Logger
import os

class BrowserManager:

    @staticmethod
    def launch_browser(playwright):
        Logger.info(f"Launching browser: {settings.BROWSER}")

        browser = getattr(playwright, settings.BROWSER).launch(
            headless=settings.HEADLESS
        )

        return browser
    
    @staticmethod
    def create_context(browser,test_name):
        Logger.info("Creating new browser context")
        os.makedirs("har",exist_ok=True)
        os.makedirs("videos",exist_ok=True)

        context = browser.new_context(
            base_url=settings.BASE_URL,
            record_har_path=f"har/{test_name}.har",
            record_video_dir="videos/"
        )

        return context
    
    @staticmethod
    def start_tracing(context):
        Logger.info("Starting trace recording")

        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

    
    @staticmethod
    def stop_tracing(context,test_name):
        os.makedirs("traces",exist_ok=True)

        trace_path = os.path.join(os.getcwd(),"traces",f"{test_name}.zip")

        Logger.info(f"Stopping trace recording -> {trace_path}")

        context.tracing.stop(path=trace_path)

        return trace_path