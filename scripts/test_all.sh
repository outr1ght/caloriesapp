#!/usr/bin/env bash
set -euo pipefail

cd backend
pytest

cd ../mobile_app
flutter test
