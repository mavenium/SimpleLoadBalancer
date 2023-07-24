from app import app

import pytest


@pytest.fixture
def client():
    """Create a fixture to yield the client"""
    with app.test_client() as client:
        yield client


def test_main(client):
    """Test the main is returning the value successfully"""
    result = client.get('/')
    assert b'application' in result.data
