import pytest


@pytest.fixture
def tag_payload():
    return {
        'name': '#tagname'
    }
