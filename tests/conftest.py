import pytest

from oriyan_portfolio import app

@pytest.fixture
def client():
    app.config.update({
        "TESTING": True,
    })
    with app.test_client() as client:
        yield client
