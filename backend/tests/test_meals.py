from tests.factories import meal_create_request_factory

def test_meal_factory_valid() -> None:
    payload = meal_create_request_factory()
    assert payload.title == "Chicken and rice"
