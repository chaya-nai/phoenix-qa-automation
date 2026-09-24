from config import BASE_URL
from utils import load_json
import pytest

test_data = load_json("data/character_data.json")

@pytest.mark.parametrize("test_data", test_data, ids=[case['tc_id'] for case in test_data])
def test_get_character(api_client, test_data):
    response = api_client.get(f"{BASE_URL}{test_data['endpoint']}")
    body = response.json()
    
    assert response.status_code == test_data['expected_http_status'], f"{test_data['tc_id']} Expect {test_data['expected_http_status']} but got {response.status_code}"
    assert body['status'] == test_data['expected_status'], f"{test_data['tc_id']} Expect {test_data['expected_status']} but got {body['status']}"
    assert body['data']['name'] == test_data['expected_name'], f"{test_data['tc_id']} Expect {test_data['expected_name']} but got {body['data']['name']}"
    assert body['data']['level'] == test_data['expected_level'], f"{test_data['tc_id']} Expect {test_data['expected_level']} but got {body['data']['level']}"
