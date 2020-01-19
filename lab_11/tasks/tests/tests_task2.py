import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from lab_11.tasks.tools.metaweather import (
    get_metaweather
)


def test_get_cities_woeid_empty_timeout():
    with patch('requests.get', side_effect=requests.exceptions.Timeout()) as mock_function:
        with pytest.raises(requests.exceptions.Timeout):
            get_cities_woeid('Warszawa', timeout=0.1)

def test_get_cities_woeid_empty_response():
    mock_respones = MagicMock()
    mock_respones.status = 200
    mock_respones.json.return_value = []

    with patch('requests.get', return_value=mock_respones) as mock_function:
        assert get_cities_woeid('Warszawa') == {}


def test_get_cities_woeid_good_response():
    mock_respones = MagicMock()
    mock_respones.status = 200
    mock_respones.json.return_value = [
        {'title': 'Warsaw',
         'location_type': 'City',
         'woeid': 523920,
         'latt_long': '52.235352,21.009390'},
        {'title': 'Newark',
         'location_type': 'City',
         'woeid': 2459269,
         'latt_long': '40.731972,-74.174179'}]

   with patch('requests.get', return_value=mock_respones) as mock_function:
        assert get_cities_woeid('War') == {
            'Warsaw': 523920,
            'Newark': 2459269,
        }


