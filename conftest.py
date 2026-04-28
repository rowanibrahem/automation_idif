import pytest
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