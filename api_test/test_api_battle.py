from config import BASE_URL
from utils import load_json
import pytest

get_data = load_json("data/character_data.json")
test_data = load_json("data/battle_data.json")

@pytest.mark.parametrize("test_data", test_data, ids=[case['tc_id'] for case in test_data])
def test_post_battle(api_client, test_data):
    before_response = api_client.get(f"{BASE_URL}{get_data[0]['endpoint']}")
    before = before_response.json()
    before_coin = before['data']['coin']
    
    response = api_client.post(f"{BASE_URL}{test_data['endpoint']}", json=test_data['payload'])
    body = response.json()
    
    after_response = api_client.get(f"{BASE_URL}{get_data[0]['endpoint']}")
    after = after_response.json()
    after_coin = after['data']['coin']
    
    
    assert response.status_code == test_data['expected_http_status'], f"{test_data['tc_id']} Expect HTTP status {test_data['expected_http_status']} but got {response.status_code}"
    assert body['status'] == test_data['expected_status'], f"{test_data['tc_id']} Expect status {test_data['expected_status']} but got {body['status']}"
    assert body['message'] == test_data['expected_message'], f"{test_data['tc_id']} Expect message {test_data['expected_message']} but got {body['message']}"
    
    if response.status_code == 200:
        assert "reward" in body, f"{test_data['tc_id']} Expected reward field"
        assert 50 <= body["reward"] <= 100, f"{test_data['tc_id']} Expected reward between 50-100 but got {body['reward']}"
        
        assert after_coin == before_coin + body['reward'] ,f"{test_data['tc_id']} Expect {before_coin + body['reward']} but got {after_coin}"
    else:
        assert "reward" not in body, f"{test_data['tc_id']} Expect no reward but got {body}"
        assert after_coin == before_coin, f"{test_data['tc_id']} Expect {before_coin} but got {after_coin}" 
    
    