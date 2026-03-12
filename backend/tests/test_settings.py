from app.schemas.settings import UserSettingsUpdateRequest

def test_settings_update_payload() -> None:
    payload = UserSettingsUpdateRequest(language="en", unit_system="metric", notifications_enabled=True)
    assert payload.model_dump(exclude_none=True)["language"].value == "en"
