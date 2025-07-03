#!/usr/bin/env bash
# Drive the whole round-trip: create → migrate → verify
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 1. generate old_state.json under AutoGen-0.4.7
./venv_047/bin/python generate_state_047.py old_state.json

# 2. migrate to 0.6.2 layout (pure stdlib, same interpreter is fine)
./venv_047/bin/python migrate_state.py old_state.json migrated_state.json

# 3. validate with AutoGen-0.6.2
./venv_062/bin/python verify_state_062.py migrated_state.json
