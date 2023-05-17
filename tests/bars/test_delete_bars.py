import pytest
from rest_framework import status
from model_bakery.baker import make

from bars.models import Address, Bars
from tests.fixtures import api_client
from .fixtures import bars_payload, address_payload
from .urls import get_bars_detail_url


@pytest.mark.xfail
def test_delete_success():
    assert False


@pytest.mark.xfail
def test_delete_nonexisting_bars_fail():
    # try to delete by id that does not exist
    assert False
