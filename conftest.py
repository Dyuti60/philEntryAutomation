import pytest
from playwright.sync_api import sync_playwright
from config.settings import settings
from datetime import datetime
import os
import allure
from core.network_logger import NetworkLogger
import json
from core.browser_manager import BrowserManager
from core.injection_registry import InjectionRegistry

# ========================
# Playwright Session Setup
# ========================

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


# ========================
# Browser Fixture
# ========================

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = BrowserManager.launch_browser(playwright_instance)
    yield browser
    browser.close()


# ========================
# Context Fixture
# ========================

@pytest.fixture
def context(browser,request):
    print("DEBUG BASE_URL:", settings.BASE_URL)

    test_name = request.node.name
    context = BrowserManager.create_context(browser, test_name)

    BrowserManager.start_tracing(context)

    yield context

    BrowserManager.stop_tracing(context, test_name)
    context.close()


# ========================
# Page Fixture
# ========================

@pytest.fixture
def page(context):
    page = context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    yield page

# ========================
# Network Logger Fixture
# ========================

@pytest.fixture
def network_logger(page):
    net_logger = NetworkLogger(page)
    net_logger.start()
    return net_logger


# ========================
# API Context Fixture
# ========================

@pytest.fixture
def api_context(playwright_instance):
    request_context = playwright_instance.request.new_context(
        base_url=settings.API_BASE_URL
    )
    yield request_context
    request_context.dispose()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    marker = item.get_closest_marker("injection")

    if marker:
        page= item.funcargs.get("page",None)

        if page:
            registry = InjectionRegistry(page)
            registry.apply(marker.args[0])

# ========================
# Failure Hook (Screenshot + Trace + Network Logs)
# ========================

@pytest.hookimpl(tryfirst=True,hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        # context = item.funcargs.get("context",None)

        ## screenshot on failure
        if page:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir,exist_ok=True)

            timestamp= datetime.now().strftime("%Y%m%d_%H%M%S")

            test_name = item.name

            file_path = os.path.join(screenshots_dir,f"{test_name}_{timestamp}.png")

            page.screenshot(path=file_path)

            print(f"📸 Screenshot saved at: {file_path}")

        #trace zip file on failure
        trace_file = os.path.join("traces", f"{item.name}.zip")
        if os.path.exists(trace_file):
            allure.attach.file(
                trace_file,
                name="Playwright Trace",
                attachment_type=allure.attachment_type.ZIP
            )

        #network logger on failure
        network_logger = item.funcargs.get("network_logger",None)

        # failure for >500 server error
        if network_logger and NetworkLogger.has_server_error():
            pytest.fail("Test failed due to 5xx server error.")

        # for other status code
        if page and network_logger:
            logs = network_logger.get_logs()

            if logs:
                allure.attach(
                    json.dumps(logs,indent=2),
                    name="Network logs",
                    attachment_type=allure.attachment_type.JSON
                )

        #attach video
        if page and page.video:
            video_path = page.video.path()
            if(os.path.exists(video_path)):
                allure.attach.file(
                    video_path,
                    name="ExecutionVideo",
                    attachment_type=allure.attachment_type.WEBM
                )
        
        


# ========================
# Attach Application Logs
# ========================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    log_file = os.path.join(os.getcwd(),"logs","app.log")

    if os.path.exists(log_file):
        allure.attach.file(log_file,name="Application Logs", attachment_type=allure.attachment_type.TEXT)


