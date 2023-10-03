import pytest

from achievements.constants import ACHIEVEMENTS


@pytest.fixture
def number_of_achievemnts():
    return len(ACHIEVEMENTS)
