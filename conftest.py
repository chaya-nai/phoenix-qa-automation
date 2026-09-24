import pytest, requests
from config import BASE_URL

@pytest.fixture
def reset():
    response = requests.post(f"{BASE_URL}/api/test/reset")
    assert response.status_code == 200

@pytest.fixture
def add_iron(reset):
    response = requests.post(f"{BASE_URL}/api/shop/buy", json={"item": "Iron Armor"})
    assert response.status_code == 200
    
@pytest.fixture
def setup_equip_iron(reset):
    buy_iron = requests.post(f"{BASE_URL}/api/shop/buy", json={"item": "Iron Armor"})
    assert buy_iron.status_code == 200
    equip_iron = requests.post(f"{BASE_URL}/api/inventory/equip", json={"item": "Iron Armor"})
    assert equip_iron.status_code == 200