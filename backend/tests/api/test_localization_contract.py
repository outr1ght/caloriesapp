import pytest


@pytest.mark.usefixtures("auth_overrides")
def test_localization_locales_include_mobile_supported_set(client):
    response = client.get('/api/v1/localization/locales')
    assert response.status_code == 200

    items = response.json()['data']
    codes = {item['code'] for item in items}
    assert {'en', 'es', 'de', 'fr', 'ru'}.issubset(codes)
