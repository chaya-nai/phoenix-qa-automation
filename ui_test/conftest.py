import pytest, requests
from playwright.sync_api import sync_playwright
from config import BASE_URL
import os
from pytest_html import extras
import base64

os.makedirs("screenshots", exist_ok=True)
os.makedirs("traces", exist_ok=True)


@pytest.fixture
def page(request):
    with sync_playwright() as p:
        is_ci = os.getenv("CI") == "true"
        browser = p.chromium.launch(headless=is_ci)
        context = browser.new_context() #test isolation แยกคุกกี้
        context.tracing.start(screenshots=True,snapshots=True,sources=True)
        page = context.new_page()
        request.node.page = page
        yield page
        
        call_report = getattr(request.node, "rep_call", None)
        if call_report and call_report.failed:
            context.tracing.stop(path=f"traces/{request.node.name}.zip")
        else:
            context.tracing.stop()
        context.close()
        browser.close()

@pytest.fixture
def setup_swap_armor(reset):
    buy_iron = requests.post(f"{BASE_URL}/api/shop/buy", json={"item": "Iron Armor"})
    assert buy_iron.status_code == 200
    buy_leather = requests.post(f"{BASE_URL}/api/shop/buy", json={"item": "Leather Armor"})
    assert buy_leather.status_code == 200
    equip_iron = requests.post(f"{BASE_URL}/api/inventory/equip", json={"item": "Iron Armor"})
    assert equip_iron.status_code == 200
    
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    page = getattr(item, "page", None)
    if report.when == "call" and report.failed and page:
        screenshot_path = f"screenshots/{item.name}.png"
        screenshot = page.screenshot(path=screenshot_path)
        screenshot_base64 = base64.b64encode(screenshot).decode("utf-8")
        
        report.extras = getattr(report, "extras", [])
        report.extras.append(extras.image(screenshot_base64))
    setattr(item, f"rep_{report.when}", report)