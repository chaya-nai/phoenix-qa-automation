from playwright.sync_api import sync_playwright,expect
from config import BASE_URL

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto(f"{BASE_URL}/login")
    
    page.locator("#username").fill("Nai")
    page.locator("#password").fill("9999")
    page.get_by_role('button', name="Login").click()
    
    
    expect(page.get_by_text("200 Login Success")).to_be_visible()
    
    
    browser.close()