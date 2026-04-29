import pytest
import time
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    """فيكستشر للمتصفح"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False عشان تشوفي المتصفح
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            import os
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            screenshot_path = f"screenshots/failure_{item.name}_{int(time.time())}.png"
            page.screenshot(path=screenshot_path)
            print(f"\n📸 Screenshot saved: {screenshot_path}")