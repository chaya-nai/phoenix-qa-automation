from playwright.sync_api import expect
from config import BASE_URL
import pytest
import requests
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_equip_iron_armor(page, add_iron):
    inventory = InventoryPage(page)
    inventory.open()
    
    expect(inventory.coin()).to_have_text("200")
    expect(inventory.equipped_outfit()).to_have_text("None")
    iron_armor = inventory.item("Iron Armor")
    expect(iron_armor).to_be_visible()
    
    inventory.equip("Iron Armor")
    expect(inventory.equip_result()).to_have_text("Equip Success")
    
    expect(iron_armor).not_to_be_visible()
    expect(inventory.equipped_outfit()).to_have_text("Iron Armor")
    expect(inventory.coin()).to_have_text("200")
    
    response = requests.get(f"{BASE_URL}/api/character")
    body = response.json()
    
    ui_coin = inventory.get_coin()
    ui_outfit = inventory.get_equipped_outfit()
    assert body['data']['coin'] == ui_coin, f"Expect coin {ui_coin} but got {body['data']['coin']}"
    assert body['data']['owned_items'] == [], f"Expect no item in inventory but got {body['data']['owned_items']}"
    assert body['data']['equipped_outfit'] == ui_outfit, f"Expect outfit {ui_outfit} but got {body['data']['equipped_outfit']}"

@pytest.mark.smoke
def test_swap_armor(page, setup_swap_armor):
    inventory = InventoryPage(page)
    inventory.open()
    
    expect(inventory.coin()).to_have_text("50")
    expect(inventory.equipped_outfit()).to_have_text("Iron Armor")
    leather_armor = inventory.item("Leather Armor")
    expect(leather_armor).to_be_visible()
    
    inventory.equip("Leather Armor")
    
    expect(inventory.equip_result()).to_have_text("Equip Success")
    expect(inventory.equipped_outfit()).to_have_text("Leather Armor")
    expect(inventory.item("Iron Armor")).to_be_visible()
    expect(leather_armor).not_to_be_visible()
    expect(inventory.coin()).to_have_text("50")
    
    response = requests.get(f"{BASE_URL}/api/character")
    body = response.json()
    
    ui_coin = inventory.get_coin()
    ui_outfit = inventory.get_equipped_outfit()
    assert body['data']['coin'] == ui_coin, f"Expect coin {ui_coin} but got {body['data']['coin']}"
    assert body['data']['owned_items'] == ["Iron Armor"], f"Expect inventory ['Iron Armor'] but got {body['data']['owned_items']}"
    assert body['data']['equipped_outfit'] == ui_outfit, f"Expect equip {ui_outfit} but got {body['data']['equipped_outfit']}"
    

@pytest.mark.parametrize("tc_id, payload, expected_status, expected_message",
    [
        ("TC_01", {"item": "Leather Armor"}, 400, "Item Not In Inventory"),
        ("TC_02", {"item": ""}, 400, "Item Not In Inventory"),
        ("TC_03", {}, 400, "Missing Item"),
    ],
)
def test_equip_invalid_item(page, tc_id, add_iron, payload, expected_status, expected_message):
    response = requests.post(f"{BASE_URL}/api/inventory/equip", json=payload)
    body = response.json()
    
    assert response.status_code == expected_status, f"{tc_id} Expect HTTP {expected_status} but got {response.status_code}"
    assert body["status"] == expected_status, f"{tc_id} Expect status {expected_status} but got {body['status']}"
    assert body["message"] == expected_message, f"{tc_id} Expect message {expected_message} but got {body['message']}"
    
    character_response = requests.get(f"{BASE_URL}/api/character")
    character_body = character_response.json()
    
    assert character_body['data']['coin'] == 200, f"{tc_id} Expect coin 200 but got {character_body['data']['coin']}"
    assert character_body['data']['owned_items'] == ["Iron Armor"], f"{tc_id} Expect Iron Armor in inventory but got {character_body['data']['owned_items']}"
    assert character_body['data']['equipped_outfit'] is None, f"{tc_id} Expect None but got {character_body['data']['equipped_outfit']}"
    
def test_equip_already_equipped_item(page, setup_equip_iron):
    response = requests.post(f"{BASE_URL}/api/inventory/equip", json={"item": "Iron Armor"})
    body = response.json()
    
    assert response.status_code == 400, f"Expect HTTP 400 but got {response.status_code}"
    assert body["status"] == 400, f"Expect status 400 but got {body['status']}"
    assert body["message"] == "Item Not In Inventory", f"Expect message Item Not In Inventory but got {body['message']}"
    
    character_response = requests.get(f"{BASE_URL}/api/character")
    character_body = character_response.json()
    assert character_body['data']['coin'] == 200, f"Expect coin 200 but got {character_body['data']['coin']}"
    assert character_body['data']['owned_items'] == [], f"Expect empty inventory but got {character_body['data']['owned_items']}"
    assert character_body['data']['equipped_outfit'] == "Iron Armor", f"Expect Iron Armor but got {character_body['data']['equipped_outfit']}"