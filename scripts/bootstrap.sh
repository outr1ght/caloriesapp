#!/usr/bin/env bash
set -euo pipefail

cd backend
alembic upgrade head
python -m scripts.seed_data
