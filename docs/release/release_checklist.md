# Release Checklist

## Pre-Release Engineering
- Run CI on main branch and ensure all jobs pass.
- Verify backend migrations apply on clean database.
- Verify docker-compose stack health checks pass.
- Validate OpenAPI docs at `/docs`.
- Verify Firebase analytics/crashlytics env values are set in release configs.

## Backend Release Steps
1. Build backend and worker images.
2. Push images with semantic tag `vX.Y.Z`.
3. Apply DB migration (`alembic upgrade head`).
4. Deploy API and worker.
5. Run post-deploy smoke checks (`/healthz`, auth login, reports endpoint).

## Mobile Release Steps
1. Run `flutter pub get`.
2. Run `flutter gen-l10n`.
3. Run `flutter analyze` and `flutter test`.
4. Build signed iOS/Android artifacts.
5. Execute manual smoke test script on staging backend.

## QA Signoff Matrix
- Auth: register/login/refresh/logout
- Meals: analyze -> edit -> save -> history update
- Reports: daily/weekly/monthly values render
- Barcode: scan known code and fallback unknown
- Settings: language/unit change persists
- Disclaimers: shown on onboarding + meal analysis + settings

## Rollback Plan
- Backend: redeploy previous image tag and rollback migration only if backward-compatible.
- Mobile: phased rollout halt and revert to prior store release.

## Versioning
- Backend tag: `vMAJOR.MINOR.PATCH`.
- Mobile build number increment per store upload.
- Changelog required for every tag.
