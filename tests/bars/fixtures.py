import pytest


@pytest.fixture()
def bars_payload():
    return {
        'title': 'bars title',
        'location': {
            'type': 'Point',
            'coordinates': [20.34523, 30.234234],
        },
        'tags': {}
    }
