import pytest

import b3tojson.fetcher as fetcher

import requests


def test_get_b3_data_no_success(mocker):
    mock_get = mocker.patch.object(requests, 'get')
    mock_get.status_code = 300

    with pytest.raises(Exception):
        fetcher.get_b3_data()

    mock_get.assert_called_once_with(fetcher.B3_NEGOTIABLE_URL, stream=True)
