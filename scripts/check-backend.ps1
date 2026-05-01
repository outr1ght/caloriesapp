param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Write-Step {
    param([string]$Message)
    Write-Host "`n[check-backend] $Message" -ForegroundColor Cyan
}

function Invoke-Checked {
    param(
        [string]$Label,
        [scriptblock]$Action
    )

    Write-Step $Label
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "Step failed: $Label"
    }
}

function Invoke-BackendCmd {
    param([string]$Command)

    $backendRoot = Join-Path $ProjectRoot 'backend'
    $wrapped = "cd /d `"$backendRoot`" && call venv\Scripts\activate.bat && $Command"
    cmd.exe /c $wrapped
    if ($LASTEXITCODE -ne 0) {
        throw "Backend command failed: $Command"
    }
}

function Test-HealthEndpoint {
    $healthUrl = 'http://127.0.0.1:8000/api/v1/health'
    try {
        $response = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -ne 200) {
            throw "Health endpoint returned HTTP $($response.StatusCode)"
        }
        Write-Host "[check-backend] Health check ok: $healthUrl" -ForegroundColor Green
    }
    catch {
        $webResponse = $_.Exception.Response
        if ($null -eq $webResponse) {
            Write-Host "[check-backend] Health check skipped: backend is not running on 127.0.0.1:8000" -ForegroundColor Yellow
            return
        }
        throw
    }
}

$composeFile = Join-Path $ProjectRoot 'infrastructure\docker-compose.yml'
$venvPython = Join-Path $ProjectRoot 'backend\venv\Scripts\python.exe'
$envPath = Join-Path $ProjectRoot 'backend\.env'
$envExamplePath = Join-Path $ProjectRoot 'backend\.env.example'

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'docker was not found in PATH.'
}

if (-not (Test-Path $composeFile)) {
    throw "Compose file not found: $composeFile"
}

if (-not (Test-Path $venvPython)) {
    throw "Backend virtual environment not found: $venvPython"
}

if ((-not (Test-Path $envPath)) -and (Test-Path $envExamplePath)) {
    Write-Step 'Creating backend/.env from backend/.env.example'
    Copy-Item $envExamplePath $envPath
}

$dockerConfigPath = Join-Path $env:TEMP 'codex-docker-config'
if (-not (Test-Path $dockerConfigPath)) {
    New-Item -ItemType Directory -Path $dockerConfigPath | Out-Null
}
$env:DOCKER_CONFIG = $dockerConfigPath

Invoke-Checked 'Starting local Docker infrastructure (postgres, redis, minio)' {
    docker compose -f $composeFile up -d postgres redis minio
}

Invoke-Checked 'Running alembic upgrade head' {
    Invoke-BackendCmd 'alembic upgrade head'
}

Invoke-Checked 'Running alembic current' {
    Invoke-BackendCmd 'alembic current'
}

Invoke-Checked 'Running backend test suite' {
    Invoke-BackendCmd 'python -m pytest'
}

Write-Step 'Checking optional health endpoint'
Test-HealthEndpoint

Write-Host "`n[check-backend] Backend quality gate passed." -ForegroundColor Green
