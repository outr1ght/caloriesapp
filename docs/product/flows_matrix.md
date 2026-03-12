# Flow Matrix

## 1. First launch onboarding
- Steps: open app -> read value/disclaimer -> continue
- Screens: splash, onboarding
- Events: app_opened, onboarding_completed
- Entities: user_settings
- Edge cases: offline, missing locale
- States: loading bootstrap, error retry

## 2. Account registration/login
- Steps: enter credentials or OAuth -> receive tokens
- Screens: auth
- Events: auth_register/auth_login
- Entities: users, auth_identities
- Edge: invalid credentials, duplicate email
- States: loading button, inline error

## 3. Profile creation
- Steps: fill demographics -> save
- Screens: profile setup
- Events: profile_updated
- Entities: user_profiles
- Edge: invalid ranges

## 4. Goal setup
- Steps: set calorie/macro goals
- Screens: goal setup
- Events: goals_updated
- Entities: nutrition_goals

## 5. Camera capture of meal
- Steps: open camera -> capture
- Screens: capture
- Events: photo_captured
- Entities: uploaded_images

## 6. Photo upload and analysis
- Steps: upload -> backend analysis
- Screens: preview, analysis
- Events: meal_photo_uploaded, meal_analysis_completed
- Entities: uploaded_images
- Edge: unsupported mime/oversize/timeout

## 7. Review and correction
- Steps: edit ingredient names/grams
- Screens: analysis editor
- Events: meal_analysis_corrected
- Entities: meal_items

## 8. Save meal
- Steps: confirm -> save
- Screens: analysis, dashboard
- Events: meal_saved
- Entities: meals, meal_items

## 9. Daily dashboard
- Steps: open home
- Screens: dashboard
- Events: dashboard_viewed
- Entities: meals, goals

## 10. Weekly/monthly reports
- Steps: select range
- Screens: reports
- Events: report_viewed
- Entities: meals, meal_items, goals

## 11. Get recommendations
- Steps: open recommendations -> generate
- Screens: recommendations
- Events: recommendation_generated
- Entities: recommendations

## 12. Barcode scan
- Steps: scan code -> lookup -> confirm save
- Screens: barcode
- Events: barcode_scanned
- Entities: barcodes, food_products
- Edge: not found fallback manual

## 13. Log weight
- Steps: add weight
- Screens: weight tracking
- Events: weight_logged
- Entities: weight_logs

## 14. Generate meal plan
- Steps: generate -> review -> optionally save
- Screens: meal planner
- Events: meal_plan_generated
- Entities: meal_plans

## 15. Change language
- Steps: settings -> locale switch
- Screens: settings, language
- Events: locale_changed
- Entities: user_settings

## 16. Change calorie target
- Steps: settings/goals -> update target
- Screens: goal setup/settings
- Events: goals_updated
- Entities: nutrition_goals

## 17. Edit past entries
- Steps: diary -> open meal -> edit/delete
- Screens: diary, meal editor
- Events: meal_updated/meal_deleted
- Entities: meals, meal_items
