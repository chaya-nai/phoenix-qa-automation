from playwright.sync_api import expect
import requests
from config import BASE_URL
from pages.shop_page import ShopPage
import pytest

@pytest.mark.serial
@pytest.mark.smoke
def test_buy_iron_armor(reset, page):
    shop = ShopPage(page)
    shop.open()
    
    expect(shop.coin()).to_have_text("500")
    
    before_coin = shop.get_coin()
    
    shop.buy("Iron Armor")
    expect(shop.result()).to_have_text("Purchase Success")
    
    price = shop.get_price("Iron Armor")
    expected_coin = before_coin - price
    
    expect(shop.coin()).to_have_text(str(expected_coin))
    after_coin = shop.get_coin()
    
    assert after_coin == expected_coin
    
    response = requests.get(f"{BASE_URL}/api/character")
    body = response.json()
    
    assert "Iron Armor" in body['data']['owned_items'], f"Expect Iron Armor in Inventory but got {body['data']['owned_items']}"
    assert body['data']['equipped_outfit'] is None, f"Expect equip nothing but got {body['data']['equipped_outfit']}"