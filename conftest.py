import pytest
import time
import os
from datetime import datetime
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

# سكرين شوت تلقائي عند الفشل
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            
            # إنشاء مجلد للشاشات لو مش موجود
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            
            # اسم الملف مع الوقت
            timestamp = int(time.time())
            screenshot_path = f"screenshots/failure_{item.name}_{timestamp}.png"
            page.screenshot(path=screenshot_path)
            print(f"\n📸 Screenshot saved: {screenshot_path}")


# إضافة معلومات في التقرير
def pytest_html_report_title(report):
    report.title = "Test Report - Final Products"


@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_header(cells):
    cells.insert(2, '<th>Execution Time</th>')
    cells.insert(3, '<th>Test Data</th>')


@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_row(report, cells):
    if hasattr(report, 'duration'):
        cells.insert(2, f'<td>{report.duration:.2f} sec</td>')
    else:
        cells.insert(2, '<td>N/A</td>')
    
    if hasattr(report, 'test_data'):
        cells.insert(3, f'<td>{report.test_data}</td>')
    else:
        cells.insert(3, '<td>-</td>')