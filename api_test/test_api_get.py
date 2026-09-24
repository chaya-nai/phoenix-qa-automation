from config import BASE_URL
from utils import load_json
import pytest

test_data = load_json("data/get_api_data.json")

@pytest.mark.parametrize("test_data", test_data, ids=[case['tc_id'] for case in test_data])
def test_api_get(api_client, test_data):
    response = api_client.get(f"{BASE_URL}{test_data['endpoint']}")
    body = response.json()
    
    assert response.status_code == test_data['expected_http_status'], f"{test_data['tc_id']} Expected HTTP status {test_data['expected_http_status']} but got {response.status_code}"
    assert body['status'] == test_data['expected_status'], f"{test_data['tc_id']} Expected JSON status {test_data['expected_status']} but got {body['status']}"
    assert body['message'] == test_data['expected_message'], f"{test_data['tc_id']} Expected JSON message {test_data['expected_message']} but got {body['message']}"