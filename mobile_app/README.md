# Calories Mobile App

Flutter client for CaloriesApp.

## Stack
- Flutter
- Riverpod
- go_router
- Dio
- flutter_secure_storage
- camera/image_picker/mobile_scanner
- fl_chart

## Setup
```bash
flutter pub get
flutter gen-l10n
```

## Run
Android emulator (default backend URL):
```bash
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1
```

Physical device / iOS simulator example:
```bash
flutter run --dart-define=API_BASE_URL=http://localhost:8000/api/v1
```

## Tests
```bash
flutter test
```

## Main flows covered
- onboarding/auth/session restore
- profile setup + goals
- meal capture/upload/analysis/save
- barcode lookup/save-as-meal
- diary CRUD (list/detail/edit/delete)
- reports/recommendations/meal planner/weights/settings

## Localization
- ARB locales: `en`, `es`, `de`, `fr`, `ru`
- Language can be changed in settings.

## Known limitations
- Requires backend + postgres + redis running.
- Camera/barcode capabilities depend on device permissions.
