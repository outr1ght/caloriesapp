param(
    [string]$SchemaPath = "docs/openapi/openapi.json",
    [string]$OutputDir = "mobile_app/lib/data/api/generated"
)

$ErrorActionPreference = "Stop"

function Write-Step([string]$Message) {
    Write-Host "[generate-flutter-api-client] $Message"
}

$root = Split-Path -Parent $PSScriptRoot
$schemaFullPath = Join-Path $root $SchemaPath
$outputFullDir = Join-Path $root $OutputDir

if (-not (Test-Path $schemaFullPath)) {
    throw "OpenAPI schema not found: $schemaFullPath"
}

$schema = Get-Content $schemaFullPath -Raw | ConvertFrom-Json
$requiredPaths = @('/api/v1/auth/login', '/api/v1/auth/register', '/api/v1/auth/logout', '/api/v1/meals', '/api/v1/meals/{meal_id}')
foreach ($path in $requiredPaths) {
    if (-not $schema.paths.PSObject.Properties.Name.Contains($path)) {
        throw "Missing required OpenAPI path: $path"
    }
}

New-Item -ItemType Directory -Force -Path $outputFullDir | Out-Null

$files = @('openapi_models.dart', 'openapi_auth_api.dart', 'openapi_meals_api.dart', 'generated.dart')
foreach ($name in $files) {
    $source = Join-Path $PSScriptRoot "flutter_codegen_templates\$name"
    if (-not (Test-Path $source)) {
        throw "Template not found: $source"
    }
    Copy-Item $source (Join-Path $outputFullDir $name) -Force
}

Write-Step "Generation completed"
Write-Host ("output_dir={0}" -f $outputFullDir)
