param(
    [string]$OutputPath = "docs/openapi/openapi.json"
)

$ErrorActionPreference = "Stop"

function Write-Step([string]$Message) {
    Write-Host "[export-openapi] $Message"
}

$root = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $root "backend"
$pythonExe = Join-Path $backendDir "venv\Scripts\python.exe"
$outputFullPath = Join-Path $root $OutputPath
$outputDir = Split-Path -Parent $outputFullPath
$backendEnv = Join-Path $backendDir ".env"

if (-not (Test-Path $pythonExe)) {
    throw "Backend virtualenv Python not found: $pythonExe"
}
if (-not (Test-Path $backendEnv)) {
    throw "Backend env file not found: $backendEnv"
}

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

Write-Step "Exporting OpenAPI schema to $outputFullPath"
$script = @"
import json
import os
import sys
from pathlib import Path

root = Path(r'$root')
backend_dir = root / 'backend'
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

from app.main import app

schema = app.openapi()
out_path = Path(r'$outputFullPath')
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding='utf-8')
print(out_path)
"@

$script | & $pythonExe -

Write-Step "Validating generated JSON"
$schema = Get-Content $outputFullPath -Raw | ConvertFrom-Json

$requiredPaths = @(
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/refresh",
    "/api/v1/auth/logout",
    "/api/v1/meals",
    "/api/v1/meals/{meal_id}"
)

foreach ($path in $requiredPaths) {
    if (-not $schema.paths.PSObject.Properties.Name.Contains($path)) {
        throw "Missing required OpenAPI path: $path"
    }
}

$componentNames = @()
if ($schema.components -and $schema.components.schemas) {
    $componentNames = @($schema.components.schemas.PSObject.Properties.Name)
}

$requiredSchemas = @(
    "PaginationMeta",
    "MealReadResponse",
    "MealListEnvelopeResponse",
    "MealListDataResponse"
)

foreach ($name in $requiredSchemas) {
    if ($componentNames -notcontains $name) {
        throw "Missing required OpenAPI schema: $name"
    }
}

$errorSchemas = @($componentNames | Where-Object { $_ -in @("HTTPValidationError", "ValidationError") -or $_ -match 'Error' })
$errorEnvelopeAvailable = $errorSchemas.Count -gt 0

Write-Step "Validation succeeded"
Write-Host ("output={0}" -f $outputFullPath)
Write-Host ("paths_ok={0}" -f ($requiredPaths -join ","))
Write-Host ("pagination_schema=PaginationMeta")
Write-Host ("meal_schemas=MealReadResponse,MealListEnvelopeResponse,MealListDataResponse")
Write-Host ("error_schemas_available={0}" -f $errorEnvelopeAvailable)
