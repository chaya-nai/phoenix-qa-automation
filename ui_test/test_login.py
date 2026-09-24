from playwright.sync_api import expect
from utils import load_json
import pytest
from config import BASE_URL
from pages.login_page import LoginPage


test_data = load_json("data/login_ui_data.json")

@pytest.mark.parametrize("test_data", test_data, ids=[case['tc_id'] for case in test_data])
def test_login(reset, page, test_data):
    login = LoginPage(page)
    login.open()
    
    login.input_username(test_data['username'])
    login.input_password(test_data['password'])
    login.login()
    
    expect(login.message(test_data['expected_message'])).to_be_visible()