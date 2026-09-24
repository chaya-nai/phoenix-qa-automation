from config import BASE_URL

def test_api_status(api_client):
    
    response = api_client.get(f"{BASE_URL}/api/status")
    body = response.json()
    
    assert response.status_code == 200, f"Expected HTTP status 200 but got {response.status_code}"
    assert body['status'] == 200, f"Expected JSON status 200 but got {body['status']}"
    assert body['message'] == "Server is running", f"Expected JSON message Server is running but got {body['message']}"