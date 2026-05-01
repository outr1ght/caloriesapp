# Upload / Storage Audit

## Контекст проверки

В рамках аудита выполнены:

- `python -m pytest` -> `83 passed in 1.11s`
- `./scripts/check-backend.ps1` -> `passed`

Это подтверждает, что базовый backend runtime, миграции и существующие тесты находятся в рабочем состоянии. Ни backend-код, ни API-контракты в рамках данного шага не изменялись.

## Что уже реализовано

### Upload endpoints

В backend реализованы два основных endpoint’а:

- `POST /api/v1/uploads/init` в `backend/app/api/routes/v1/uploads.py`
- `POST /api/v1/uploads/complete` в `backend/app/api/routes/v1/uploads.py`

Оба endpoint’а работают в рамках существующего response envelope и защищены аутентификацией. Для них также применён rate limiting через общий пользовательский limiter.

### Валидация запроса на upload

В `backend/app/core/upload_security.py` уже реализована серверная валидация метаданных upload:

- проверка `filename` по regex `^[A-Za-z0-9._-]{1,255}$`
- allowlist MIME-типов через `APP_ALLOWED_UPLOAD_MIME`
- ограничение размера файла через `APP_MAX_UPLOAD_BYTES`
- проверка, что `file_size > 0`
- проверка формата `sha256` как 64-символьной hex-строки

По умолчанию поддерживаются:

- `image/jpeg`
- `image/png`
- `image/webp`

### Storage abstraction

S3/MinIO abstraction реализован в `backend/app/integrations/storage_s3.py`:

- инициализация через env-based config
- генерация presigned PUT URL
- проверка существования объекта через `head_object`
- преобразование storage-side ошибок в `AppException(..., status_code=503)`

### Конфигурация локального storage

В `.env.example` и `infrastructure/docker-compose.yml` уже предусмотрен локальный MinIO-path:

- `APP_S3_ENDPOINT_URL=http://localhost:9000`
- `APP_S3_BUCKET=nutrition-assets`
- `APP_S3_ACCESS_KEY_ID=minioadmin`
- `APP_S3_SECRET_ACCESS_KEY=minioadmin`
- `APP_S3_USE_SSL=false`

Это делает локальную проверку upload/storage-потока воспроизводимой в dev-среде.

## Сильные стороны текущей реализации

### Низкий риск path traversal и overwrite по пользовательскому имени файла

Storage key формируется на backend стороне в `UploadService.init_upload()` по шаблону:

- `users/{user_id}/uploads/{upload_id}.{ext}`

За счёт этого:

- путь не берётся напрямую из пользовательского ввода
- используется backend-generated `upload_id`
- storage key namespaced по `user_id`
- присутствует дополнительная защита через ограничение имени файла regex’ом
- в модели `UploadedImage` есть уникальность по `storage_key`

Это существенно снижает риск path traversal и случайного overwrite.

### Presigned upload вместо проксирования файла через backend

Backend не принимает бинарный файл напрямую, а выдаёт presigned URL. Это снижает нагрузку на приложение и упрощает горизонтальное масштабирование upload path.

### Ошибки storage не раскрывают внутренние детали

Storage-ошибки преобразуются в контролируемые application exceptions. Это хорошо с точки зрения безопасности и согласованности API-ответов.

## Основные риски и пробелы

### 1. Нет проверки соответствия extension и MIME

Сейчас backend валидирует MIME-тип и отдельно ограничивает `filename`, но не проверяет, что расширение файла согласовано с заявленным `content_type`.

Пример риска:

- пользователь может отправить `file.png` с `image/jpeg`
- backend примет метаданные, а storage key будет построен из расширения имени файла

Это не даёт немедленного path traversal риска, но создаёт неоднозначность в storage semantics и downstream-обработке.

### 2. Нет content verification после upload

Текущий flow не проверяет фактическое содержимое загруженного объекта:

- нет magic-byte/sniffing validation
- нет проверки, что объект действительно является JPEG/PNG/WEBP
- нет проверки, что фактический checksum объекта совпадает с переданным `sha256`

Сейчас `sha256` валидируется только по формату строки, но не используется для post-upload integrity verification.

Это главный функциональный пробел для production hardening upload-контура.

### 3. Есть риск orphaned upload records

В `UploadService.init_upload()` DB-record создаётся и коммитится до генерации presigned URL. Если генерация presigned URL завершится ошибкой после commit, в базе может остаться orphaned upload record без успешно завершённого upload flow.

Также отсутствует явная cleanup-стратегия для случаев:

- presigned URL выдан, но файл не был загружен
- объект не существует на шаге `complete`
- объект загружен, но не привязан к дальнейшему meal flow
- upload заброшен пользователем

### 4. Cleanup lifecycle отсутствует

В текущем коде не видно механизма:

- удаления просроченных/неиспользованных upload records
- удаления orphaned объектов из bucket
- компенсации после частичных сбоев

Для production это создаёт риск накопления мусора и расхождения между DB и object storage.

### 5. Logging/observability для upload/storage слабые

Несмотря на наличие общего request/error logging, upload/storage слой почти не генерирует собственные structured события.

Недостаёт явных логов для:

- `presigned_url_generation_failed`
- `upload_object_missing_on_complete`
- validation reject по filename/MIME/checksum
- non-404 storage failures на `head_object`
- cleanup/dead object scenarios

Сейчас ошибки в целом корректно доходят до response envelope, но операционная наблюдаемость upload flow остаётся ограниченной.

### 6. Семантика complete ограничена проверкой существования объекта

`complete_upload()` фактически делает одно ключевое действие:

- вызывает `object_exists(storage_key)`

Если объект найден, backend помечает upload как verified через metadata, но не выполняет более глубокую integrity-проверку. Это означает, что шаг `complete` подтверждает наличие объекта, но не подтверждает корректность содержимого.

## MIME / format hardening status

### Поддерживаемые форматы

Поддержка ограничена следующими форматами:

- JPEG
- PNG
- WEBP

Это корректный и достаточно безопасный минимальный набор для food photo flow.

### Что уже защищено

- запрет произвольных MIME через allowlist
- ограничение максимального размера
- ограничение пользовательского имени файла

### Чего не хватает

- extension-to-MIME consistency check
- фактической file signature validation
- проверки post-upload integrity по checksum

## Signed / public URL behavior

Текущая реализация ориентирована на private object storage с presigned PUT URL.

Что видно по коду:

- backend выдаёт presigned URL только для upload
- явного публичного URL-поведения не реализовано
- явной стратегии download URL / signed GET URL в audited path не видно
- ACL/visibility policy объекта явно не описана на уровне application layer

Это допустимо для приватного MVP storage path, но для production желательно формализовать модель доступа к уже загруженным фото.

## Error visibility status

### Хорошо

- storage failures транслируются в контролируемые API-ошибки
- invalid MIME и oversized file уже покрыты тестами
- missing object в `complete` уже маппится в корректную business error ветку

### Недостаточно

- нет достаточно детализированных structured logs для расследования upload/storage инцидентов
- нет явной телеметрии по orphaned uploads
- нет метрик или событий по storage деградации

## Текущее покрытие тестами

### Уже покрыто

В существующих тестах есть проверки на:

- invalid MIME
- oversized file
- invalid UUID в `complete`
- missing upload record
- successful complete response path
- `object_exists()` при `404` от storage

### Не хватает тестов

Отсутствуют или слабо покрыты сценарии:

- invalid filename
- invalid `sha256` format
- mismatch между extension и MIME
- storage failure при генерации presigned URL
- non-404 error при `head_object`
- orphaned record after partial failure
- cleanup strategy для abandoned uploads
- checksum/content verification после upload

## Итоговая оценка

Текущая upload/storage реализация уже имеет рабочий и относительно безопасный базовый каркас:

- presigned uploads
- MIME allowlist
- size limits
- безопасная генерация storage key
- S3/MinIO abstraction

Однако до production hardening остаются важные пробелы:

- нет post-upload integrity verification
- нет cleanup/orphan lifecycle
- ограниченная observability
- нет проверки extension/content-type consistency

С практической точки зрения текущий контур можно считать `partially ready`: он пригоден для controlled dev/MVP flow, но ещё недостаточно защищён и операционно прозрачен для production-нагрузки.

## Recommended Next Task

Рекомендуемый следующий шаг: внедрить upload completion hardening без изменения API-контракта:

- добавить post-upload integrity validation
- добавить structured logging для storage/upload failure paths
- определить и покрыть тестами orphan/cleanup lifecycle
