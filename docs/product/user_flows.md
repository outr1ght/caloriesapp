# Product Flows

## Core Flows
Each flow includes user steps, screens, events, entities, and states.

### First launch onboarding
- Steps: open app -> select language -> consent disclaimers -> continue
- Screens: splash, onboarding
- Events: `app_opened`, `onboarding_completed`
- Entities: `user_settings`
- Edge: no network
- States: loading config, empty none, error retry CTA

### Capture and save meal
- Steps: open camera -> capture -> upload -> analyze -> edit -> save
- Screens: camera, preview, analysis, editor
- Events: `meal_photo_uploaded`, `meal_analysis_completed`, `meal_saved`
- Entities: `uploaded_images`, `meals`, `meal_items`
- Edge: low confidence, upload failure, unsupported image
- States: spinner, empty analysis, error with manual entry fallback

### Reports
- Steps: open reports -> switch range daily/weekly/monthly
- Screens: report dashboard
- Events: `report_viewed`
- Entities: `meals`, `meal_items`, `nutrition_goals`
- Edge: no data in range
- States: loading skeleton, empty tips card, error reload
