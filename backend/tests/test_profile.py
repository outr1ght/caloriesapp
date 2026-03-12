from app.schemas.profile import UserProfileUpdateRequest

def test_profile_update_payload() -> None:
    payload = UserProfileUpdateRequest(first_name="Alex", height_cm=178.5)
    assert payload.model_dump(exclude_none=True)["first_name"] == "Alex"
