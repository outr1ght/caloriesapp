param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [switch]$StartInfrastructure,
    [switch]$SkipMigrations
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-PythonCommand {
    $candidates = @(
        @{ Cmd = 'python'; Args = @() },
        @{ Cmd = 'py'; Args = @('-3.12') },
        @{ Cmd = 'py'; Args = @('-3.11') }
    )

    foreach ($candidate in $candidates) {
        try {
            $versionOutput = & $candidate.Cmd @($candidate.Args + @('--version')) 2>&1
            if ($LASTEXITCODE -ne 0) { continue }
            $match = [regex]::Match(($versionOutput | Out-String), 'Python\s+(\d+)\.(\d+)\.(\d+)')
            if (-not $match.Success) { continue }
            $major = [int]$match.Groups[1].Value
            $minor = [int]$match.Groups[2].Value
            if ($major -gt 3 -or ($major -eq 3 -and $minor -ge 11)) {
                return $candidate
            }
        }
        catch {
            continue
        }
    }

    throw 'Python 3.11+ was not found in PATH. Install Python and reopen the terminal.'
}

function Ensure-DockerCompose {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw 'Docker CLI was not found in PATH. Install Docker Desktop or run bootstrap without -StartInfrastructure.'
    }

    & docker compose version | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw 'docker compose is not available. Ensure Docker Desktop is installed and compose v2 is enabled.'
    }
}

$backendRoot = Join-Path $ProjectRoot 'backend'
$venvPath = Join-Path $backendRoot 'venv'
$requirementsPath = Join-Path $backendRoot 'requirements.txt'
$envExamplePath = Join-Path $backendRoot '.env.example'
$envPath = Join-Path $backendRoot '.env'
$composeFile = Join-Path $ProjectRoot 'infrastructure\docker-compose.yml'
$python = Get-PythonCommand

Write-Host "[bootstrap] Using project root: $ProjectRoot"
Write-Host "[bootstrap] Using backend root: $backendRoot"
Write-Host "[bootstrap] Using Python command: $($python.Cmd) $($python.Args -join ' ')"

if ((-not (Test-Path $envPath)) -and (Test-Path $envExamplePath)) {
    Write-Host '[bootstrap] Creating backend/.env from backend/.env.example'
    Copy-Item $envExamplePath $envPath
}

if ($StartInfrastructure) {
    Ensure-DockerCompose
    Write-Host '[bootstrap] Starting local infrastructure with Docker Compose'
    & docker compose -f $composeFile up -d postgres redis minio
    if ($LASTEXITCODE -ne 0) {
        throw 'Failed to start docker compose services.'
    }
}

if (Test-Path $venvPath) {
    Write-Host '[bootstrap] Removing existing backend/venv'
    Remove-Item -Recurse -Force $venvPath
}

Write-Host '[bootstrap] Creating virtual environment'
& $python.Cmd @($python.Args + @('-m', 'venv', $venvPath))
if ($LASTEXITCODE -ne 0) {
    throw 'Failed to create backend virtual environment.'
}

$venvPython = Join-Path $venvPath 'Scripts\python.exe'
if (-not (Test-Path $venvPython)) {
    throw "Virtual environment Python not found: $venvPython"
}

Write-Host '[bootstrap] Upgrading pip'
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw 'Failed to upgrade pip in backend virtual environment.'
}

Write-Host '[bootstrap] Installing backend dependencies'
& $venvPython -m pip install -r $requirementsPath
if ($LASTEXITCODE -ne 0) {
    throw 'Failed to install backend requirements.'
}

Push-Location $backendRoot
try {
    Write-Host '[bootstrap] Verifying pytest'
    & $venvPython -m pytest --version
    if ($LASTEXITCODE -ne 0) {
        throw 'pytest is not available in backend virtual environment.'
    }

    Write-Host '[bootstrap] Verifying alembic heads'
    & $venvPython -m alembic heads
    if ($LASTEXITCODE -ne 0) {
        throw 'alembic heads failed.'
    }

    if (-not $SkipMigrations) {
        Write-Host '[bootstrap] Attempting alembic upgrade head'
        try {
            & $venvPython -m alembic upgrade head
            if ($LASTEXITCODE -ne 0) {
                Write-Warning 'alembic upgrade head exited with a non-zero status.'
            }
        }
        catch {
            Write-Warning ('alembic upgrade head failed: ' + $_.Exception.Message)
        }
    }
}
finally {
    Pop-Location
}

Write-Host '[bootstrap] Backend environment is ready.'
Write-Host '[bootstrap] Activate with: backend\venv\Scripts\activate'
if ($StartInfrastructure) {
    Write-Host "[bootstrap] Infra started from: $composeFile"
}
