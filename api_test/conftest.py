import pytest, requests

@pytest.fixture
def api_client():
    session = requests.Session()
    yield session
    session.close()