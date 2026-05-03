import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_de.dart';
import 'app_localizations_en.dart';
import 'app_localizations_es.dart';
import 'app_localizations_fr.dart';
import 'app_localizations_ru.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'generated/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
      : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
    delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
  ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('de'),
    Locale('en'),
    Locale('es'),
    Locale('fr'),
    Locale('ru')
  ];

  /// No description provided for @loadingLabel.
  ///
  /// In en, this message translates to:
  /// **'Loading...'**
  String get loadingLabel;

  /// No description provided for @loginTitle.
  ///
  /// In en, this message translates to:
  /// **'Login'**
  String get loginTitle;

  /// No description provided for @signupTitle.
  ///
  /// In en, this message translates to:
  /// **'Create account'**
  String get signupTitle;

  /// No description provided for @emailLabel.
  ///
  /// In en, this message translates to:
  /// **'Email'**
  String get emailLabel;

  /// No description provided for @passwordLabel.
  ///
  /// In en, this message translates to:
  /// **'Password'**
  String get passwordLabel;

  /// No description provided for @loginAction.
  ///
  /// In en, this message translates to:
  /// **'Login'**
  String get loginAction;

  /// No description provided for @signupAction.
  ///
  /// In en, this message translates to:
  /// **'Sign up'**
  String get signupAction;

  /// No description provided for @createAccountAction.
  ///
  /// In en, this message translates to:
  /// **'Create account'**
  String get createAccountAction;

  /// No description provided for @haveAccountAction.
  ///
  /// In en, this message translates to:
  /// **'I already have an account'**
  String get haveAccountAction;

  /// No description provided for @onboardingIntroTitle.
  ///
  /// In en, this message translates to:
  /// **'Track your nutrition'**
  String get onboardingIntroTitle;

  /// No description provided for @onboardingIntroBody.
  ///
  /// In en, this message translates to:
  /// **'Capture meals and monitor calories with a clean daily workflow.'**
  String get onboardingIntroBody;

  /// No description provided for @onboardingAssistantTitle.
  ///
  /// In en, this message translates to:
  /// **'AI nutrition assistant'**
  String get onboardingAssistantTitle;

  /// No description provided for @onboardingAssistantBody.
  ///
  /// In en, this message translates to:
  /// **'Get meal insights, macro estimates, and practical recommendations.'**
  String get onboardingAssistantBody;

  /// No description provided for @onboardingCameraTitle.
  ///
  /// In en, this message translates to:
  /// **'Camera-first logging'**
  String get onboardingCameraTitle;

  /// No description provided for @onboardingCameraBody.
  ///
  /// In en, this message translates to:
  /// **'Take a photo or choose one from gallery and review analysis before saving.'**
  String get onboardingCameraBody;

  /// No description provided for @nextAction.
  ///
  /// In en, this message translates to:
  /// **'Next'**
  String get nextAction;

  /// No description provided for @getStartedAction.
  ///
  /// In en, this message translates to:
  /// **'Get started'**
  String get getStartedAction;

  /// No description provided for @continueAction.
  ///
  /// In en, this message translates to:
  /// **'Continue'**
  String get continueAction;

  /// No description provided for @profileSetupTitle.
  ///
  /// In en, this message translates to:
  /// **'Profile setup'**
  String get profileSetupTitle;

  /// No description provided for @ageLabel.
  ///
  /// In en, this message translates to:
  /// **'Age'**
  String get ageLabel;

  /// No description provided for @genderLabel.
  ///
  /// In en, this message translates to:
  /// **'Gender'**
  String get genderLabel;

  /// No description provided for @genderMale.
  ///
  /// In en, this message translates to:
  /// **'Male'**
  String get genderMale;

  /// No description provided for @genderFemale.
  ///
  /// In en, this message translates to:
  /// **'Female'**
  String get genderFemale;

  /// No description provided for @genderOther.
  ///
  /// In en, this message translates to:
  /// **'Other'**
  String get genderOther;

  /// No description provided for @heightLabel.
  ///
  /// In en, this message translates to:
  /// **'Height (cm)'**
  String get heightLabel;

  /// No description provided for @weightLabel.
  ///
  /// In en, this message translates to:
  /// **'Weight (kg)'**
  String get weightLabel;

  /// No description provided for @activityLevelLabel.
  ///
  /// In en, this message translates to:
  /// **'Activity level'**
  String get activityLevelLabel;

  /// No description provided for @activitySedentary.
  ///
  /// In en, this message translates to:
  /// **'Sedentary'**
  String get activitySedentary;

  /// No description provided for @activityLight.
  ///
  /// In en, this message translates to:
  /// **'Light'**
  String get activityLight;

  /// No description provided for @activityModerate.
  ///
  /// In en, this message translates to:
  /// **'Moderate'**
  String get activityModerate;

  /// No description provided for @activityActive.
  ///
  /// In en, this message translates to:
  /// **'Active'**
  String get activityActive;

  /// No description provided for @goalSetupTitle.
  ///
  /// In en, this message translates to:
  /// **'Goal setup'**
  String get goalSetupTitle;

  /// No description provided for @tdeeLabel.
  ///
  /// In en, this message translates to:
  /// **'Calculated TDEE'**
  String get tdeeLabel;

  /// No description provided for @calorieGoalLabel.
  ///
  /// In en, this message translates to:
  /// **'Daily calorie goal'**
  String get calorieGoalLabel;

  /// No description provided for @saveGoalAction.
  ///
  /// In en, this message translates to:
  /// **'Save goal'**
  String get saveGoalAction;

  /// No description provided for @dashboardTitle.
  ///
  /// In en, this message translates to:
  /// **'Dashboard'**
  String get dashboardTitle;

  /// No description provided for @dailyCaloriesProgressTitle.
  ///
  /// In en, this message translates to:
  /// **'Daily calories progress'**
  String get dailyCaloriesProgressTitle;

  /// No description provided for @progressCaloriesSample.
  ///
  /// In en, this message translates to:
  /// **'980 / 2200 kcal'**
  String get progressCaloriesSample;

  /// No description provided for @macroSummaryTitle.
  ///
  /// In en, this message translates to:
  /// **'Macro summary'**
  String get macroSummaryTitle;

  /// No description provided for @macroSummarySample.
  ///
  /// In en, this message translates to:
  /// **'Protein 72g | Carbs 110g | Fat 38g'**
  String get macroSummarySample;

  /// No description provided for @recentMealsTitle.
  ///
  /// In en, this message translates to:
  /// **'Recent meals'**
  String get recentMealsTitle;

  /// No description provided for @recentMealsSample.
  ///
  /// In en, this message translates to:
  /// **'Chicken bowl, Greek yogurt'**
  String get recentMealsSample;

  /// No description provided for @quickAddMealAction.
  ///
  /// In en, this message translates to:
  /// **'Quick add meal'**
  String get quickAddMealAction;

  /// No description provided for @dashboardNav.
  ///
  /// In en, this message translates to:
  /// **'Dashboard'**
  String get dashboardNav;

  /// No description provided for @diaryNav.
  ///
  /// In en, this message translates to:
  /// **'Diary'**
  String get diaryNav;

  /// No description provided for @reportsNav.
  ///
  /// In en, this message translates to:
  /// **'Reports'**
  String get reportsNav;

  /// No description provided for @settingsNav.
  ///
  /// In en, this message translates to:
  /// **'Settings'**
  String get settingsNav;

  /// No description provided for @mealCaptureTitle.
  ///
  /// In en, this message translates to:
  /// **'Meal capture'**
  String get mealCaptureTitle;

  /// No description provided for @captureWithCameraAction.
  ///
  /// In en, this message translates to:
  /// **'Capture with camera'**
  String get captureWithCameraAction;

  /// No description provided for @pickFromGalleryAction.
  ///
  /// In en, this message translates to:
  /// **'Pick from gallery'**
  String get pickFromGalleryAction;

  /// No description provided for @photoPreviewTitle.
  ///
  /// In en, this message translates to:
  /// **'Photo preview'**
  String get photoPreviewTitle;

  /// No description provided for @retakeAction.
  ///
  /// In en, this message translates to:
  /// **'Retake'**
  String get retakeAction;

  /// No description provided for @analyzeMealAction.
  ///
  /// In en, this message translates to:
  /// **'Analyze meal'**
  String get analyzeMealAction;

  /// No description provided for @mealAnalysisTitle.
  ///
  /// In en, this message translates to:
  /// **'Meal analysis'**
  String get mealAnalysisTitle;

  /// No description provided for @dishNameLabel.
  ///
  /// In en, this message translates to:
  /// **'Dish name'**
  String get dishNameLabel;

  /// No description provided for @sampleDishName.
  ///
  /// In en, this message translates to:
  /// **'Chicken rice bowl'**
  String get sampleDishName;

  /// No description provided for @estimatedWeightLabel.
  ///
  /// In en, this message translates to:
  /// **'Estimated weight'**
  String get estimatedWeightLabel;

  /// No description provided for @sampleWeightValue.
  ///
  /// In en, this message translates to:
  /// **'420 g'**
  String get sampleWeightValue;

  /// No description provided for @confidenceLabel.
  ///
  /// In en, this message translates to:
  /// **'Confidence'**
  String get confidenceLabel;

  /// No description provided for @sampleConfidenceValue.
  ///
  /// In en, this message translates to:
  /// **'0.84'**
  String get sampleConfidenceValue;

  /// No description provided for @ingredientsLabel.
  ///
  /// In en, this message translates to:
  /// **'Ingredients'**
  String get ingredientsLabel;

  /// No description provided for @newIngredientLabel.
  ///
  /// In en, this message translates to:
  /// **'New ingredient'**
  String get newIngredientLabel;

  /// No description provided for @editIngredientsAction.
  ///
  /// In en, this message translates to:
  /// **'Edit ingredients'**
  String get editIngredientsAction;

  /// No description provided for @foodDiaryTitle.
  ///
  /// In en, this message translates to:
  /// **'Food diary'**
  String get foodDiaryTitle;

  /// No description provided for @todayLabel.
  ///
  /// In en, this message translates to:
  /// **'Today'**
  String get todayLabel;

  /// No description provided for @sampleMealTitle.
  ///
  /// In en, this message translates to:
  /// **'Lunch - Chicken rice bowl'**
  String get sampleMealTitle;

  /// No description provided for @sampleMealCalories.
  ///
  /// In en, this message translates to:
  /// **'620 kcal'**
  String get sampleMealCalories;

  /// No description provided for @mealDetailTitle.
  ///
  /// In en, this message translates to:
  /// **'Meal detail'**
  String get mealDetailTitle;

  /// No description provided for @mealIdLabel.
  ///
  /// In en, this message translates to:
  /// **'Meal ID'**
  String get mealIdLabel;

  /// No description provided for @editMealAction.
  ///
  /// In en, this message translates to:
  /// **'Edit meal'**
  String get editMealAction;

  /// No description provided for @reportsTitle.
  ///
  /// In en, this message translates to:
  /// **'Nutrition reports'**
  String get reportsTitle;

  /// No description provided for @dailyReportTab.
  ///
  /// In en, this message translates to:
  /// **'Daily'**
  String get dailyReportTab;

  /// No description provided for @weeklyReportTab.
  ///
  /// In en, this message translates to:
  /// **'Weekly'**
  String get weeklyReportTab;

  /// No description provided for @monthlyReportTab.
  ///
  /// In en, this message translates to:
  /// **'Monthly'**
  String get monthlyReportTab;

  /// No description provided for @summaryCardsTitle.
  ///
  /// In en, this message translates to:
  /// **'Summary'**
  String get summaryCardsTitle;

  /// No description provided for @reportSummarySample.
  ///
  /// In en, this message translates to:
  /// **'Average 2050 kcal/day'**
  String get reportSummarySample;

  /// No description provided for @recommendationsTitle.
  ///
  /// In en, this message translates to:
  /// **'Recommendations'**
  String get recommendationsTitle;

  /// No description provided for @recommendationCardTitle.
  ///
  /// In en, this message translates to:
  /// **'Protein improvement'**
  String get recommendationCardTitle;

  /// No description provided for @recommendationCardBody.
  ///
  /// In en, this message translates to:
  /// **'Add one high-protein snack in the afternoon.'**
  String get recommendationCardBody;

  /// No description provided for @mealPlannerTitle.
  ///
  /// In en, this message translates to:
  /// **'Meal planner'**
  String get mealPlannerTitle;

  /// No description provided for @mealPlannerWeekLabel.
  ///
  /// In en, this message translates to:
  /// **'Week plan'**
  String get mealPlannerWeekLabel;

  /// No description provided for @mealPlannerSample.
  ///
  /// In en, this message translates to:
  /// **'3 balanced lunches prepared'**
  String get mealPlannerSample;

  /// No description provided for @barcodeScanTitle.
  ///
  /// In en, this message translates to:
  /// **'Barcode scan'**
  String get barcodeScanTitle;

  /// No description provided for @barcodeWaitingLabel.
  ///
  /// In en, this message translates to:
  /// **'Point camera at barcode'**
  String get barcodeWaitingLabel;

  /// No description provided for @barcodeDetectedLabel.
  ///
  /// In en, this message translates to:
  /// **'Detected'**
  String get barcodeDetectedLabel;

  /// No description provided for @weightTrackingTitle.
  ///
  /// In en, this message translates to:
  /// **'Weight tracking'**
  String get weightTrackingTitle;

  /// No description provided for @currentWeightLabel.
  ///
  /// In en, this message translates to:
  /// **'Current weight'**
  String get currentWeightLabel;

  /// No description provided for @currentWeightSample.
  ///
  /// In en, this message translates to:
  /// **'74.8 kg'**
  String get currentWeightSample;

  /// No description provided for @logWeightAction.
  ///
  /// In en, this message translates to:
  /// **'Log weight'**
  String get logWeightAction;

  /// No description provided for @settingsTitle.
  ///
  /// In en, this message translates to:
  /// **'Settings'**
  String get settingsTitle;

  /// No description provided for @languageLabel.
  ///
  /// In en, this message translates to:
  /// **'Language'**
  String get languageLabel;

  /// No description provided for @calorieGoalChangeLabel.
  ///
  /// In en, this message translates to:
  /// **'Change calorie goal'**
  String get calorieGoalChangeLabel;

  /// No description provided for @logoutAction.
  ///
  /// In en, this message translates to:
  /// **'Logout'**
  String get logoutAction;

  /// No description provided for @languageEnglish.
  ///
  /// In en, this message translates to:
  /// **'English'**
  String get languageEnglish;

  /// No description provided for @languageSpanish.
  ///
  /// In en, this message translates to:
  /// **'Spanish'**
  String get languageSpanish;

  /// No description provided for @languageGerman.
  ///
  /// In en, this message translates to:
  /// **'German'**
  String get languageGerman;

  /// No description provided for @languageFrench.
  ///
  /// In en, this message translates to:
  /// **'French'**
  String get languageFrench;

  /// No description provided for @languageRussian.
  ///
  /// In en, this message translates to:
  /// **'Russian'**
  String get languageRussian;

  /// No description provided for @markAppliedAction.
  ///
  /// In en, this message translates to:
  /// **'Mark applied'**
  String get markAppliedAction;

  /// No description provided for @genericLoadFailedLabel.
  ///
  /// In en, this message translates to:
  /// **'Unable to load data.'**
  String get genericLoadFailedLabel;

  /// No description provided for @unitImperialLabel.
  ///
  /// In en, this message translates to:
  /// **'Imperial'**
  String get unitImperialLabel;

  /// No description provided for @unitSystemLabel.
  ///
  /// In en, this message translates to:
  /// **'Unit system'**
  String get unitSystemLabel;

  /// No description provided for @genericEmptyLabel.
  ///
  /// In en, this message translates to:
  /// **'No data yet.'**
  String get genericEmptyLabel;

  /// No description provided for @dismissAction.
  ///
  /// In en, this message translates to:
  /// **'Dismiss'**
  String get dismissAction;

  /// No description provided for @unitMetricLabel.
  ///
  /// In en, this message translates to:
  /// **'Metric'**
  String get unitMetricLabel;

  /// No description provided for @carbsTargetLabel.
  ///
  /// In en, this message translates to:
  /// **'Carbs target (g)'**
  String get carbsTargetLabel;

  /// No description provided for @genericSaveFailedLabel.
  ///
  /// In en, this message translates to:
  /// **'Unable to save. Please try again.'**
  String get genericSaveFailedLabel;

  /// No description provided for @lastNameLabel.
  ///
  /// In en, this message translates to:
  /// **'Last name'**
  String get lastNameLabel;

  /// No description provided for @fatTargetLabel.
  ///
  /// In en, this message translates to:
  /// **'Fat target (g)'**
  String get fatTargetLabel;

  /// No description provided for @profileValidationMessage.
  ///
  /// In en, this message translates to:
  /// **'Please enter valid profile values.'**
  String get profileValidationMessage;

  /// No description provided for @firstNameLabel.
  ///
  /// In en, this message translates to:
  /// **'First name'**
  String get firstNameLabel;

  /// No description provided for @goalValidationMessage.
  ///
  /// In en, this message translates to:
  /// **'Please enter valid goal values.'**
  String get goalValidationMessage;

  /// No description provided for @proteinTargetLabel.
  ///
  /// In en, this message translates to:
  /// **'Protein target (g)'**
  String get proteinTargetLabel;

  /// No description provided for @saveMealAction.
  ///
  /// In en, this message translates to:
  /// **'Save meal'**
  String get saveMealAction;

  /// No description provided for @lowConfidenceTitle.
  ///
  /// In en, this message translates to:
  /// **'Low confidence detected'**
  String get lowConfidenceTitle;

  /// No description provided for @unknownBrandLabel.
  ///
  /// In en, this message translates to:
  /// **'Unknown brand'**
  String get unknownBrandLabel;

  /// No description provided for @invalidIngredientsMessage.
  ///
  /// In en, this message translates to:
  /// **'Please provide valid ingredient names before saving.'**
  String get invalidIngredientsMessage;

  /// No description provided for @lowConfidenceMessage.
  ///
  /// In en, this message translates to:
  /// **'Review ingredient names before saving this meal.'**
  String get lowConfidenceMessage;

  /// No description provided for @saveSuccessMessage.
  ///
  /// In en, this message translates to:
  /// **'Saved successfully.'**
  String get saveSuccessMessage;

  /// No description provided for @retryAction.
  ///
  /// In en, this message translates to:
  /// **'Retry'**
  String get retryAction;

  /// No description provided for @unknownProductLabel.
  ///
  /// In en, this message translates to:
  /// **'Unknown product'**
  String get unknownProductLabel;

  /// No description provided for @invalidBarcodeSaveMessage.
  ///
  /// In en, this message translates to:
  /// **'Product data is incomplete and cannot be saved.'**
  String get invalidBarcodeSaveMessage;

  /// No description provided for @barcodeNotFoundLabel.
  ///
  /// In en, this message translates to:
  /// **'No product found for this barcode.'**
  String get barcodeNotFoundLabel;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['de', 'en', 'es', 'fr', 'ru'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'de':
      return AppLocalizationsDe();
    case 'en':
      return AppLocalizationsEn();
    case 'es':
      return AppLocalizationsEs();
    case 'fr':
      return AppLocalizationsFr();
    case 'ru':
      return AppLocalizationsRu();
  }

  throw FlutterError(
      'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
      'an issue with the localizations generation tool. Please file an issue '
      'on GitHub with a reproducible sample app and the gen-l10n configuration '
      'that was used.');
}
