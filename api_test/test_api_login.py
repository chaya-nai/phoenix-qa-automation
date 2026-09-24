import pytest
from utils import load_json
from config import BASE_URL

test_data = load_json("data/login_api_data.json")

@pytest.mark.parametrize("test_data", test_data, ids=[case['tc_id'] for case in test_data])
def test_api_login(api_client, test_data):
    
    response = api_client.post(f"{BASE_URL}/api/login", json=test_data['payload'])
    body = response.json()
    
    assert response.status_code == test_data['expected_http_status'], f"Expected HTTP status {test_data['expected_http_status']} but got {response.status_code}"
    assert body['status'] == test_data['expected_status'], f"Expected JSON status {test_data['expected_status']} but got {body['status']}"
    assert body['message'] == test_data['expected_message'], f"Expected JSON message {test_data['expected_message']} but got {body['message']}"