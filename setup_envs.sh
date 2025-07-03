#!/usr/bin/env bash
# setup_envs_uv.sh
# ---------------------------------------------------------------------------
# Build two isolated virtual-envs with uv, one for AutoGen-0.4.7 and one for
# AutoGen-0.6.2, each including autogen-ext with the openai extras.
# ---------------------------------------------------------------------------

set -euo pipefail

# ── 1. sanity check ──────────────────────────────────────────────────────────
if ! command -v uv >/dev/null 2>&1; then
  echo "❌  'uv' not found. Install it first:"
  echo "    curl -Ls https://install.uv.link | sh"
  exit 1
fi

# ── 2. helper ---------------------------------------------------------------
# $1 = venv directory   $2 = version (e.g. 0.4.7)
make_env () {
  local venv_dir=$1
  local ver=$2

  echo "🔧 Making ${venv_dir} (AutoGen ${ver}) …"
  uv venv "${venv_dir}"

  # Activate the env so that subsequent uv pip calls target it.
  # shellcheck disable=SC1090
  source "${venv_dir}/bin/activate"

  # Upgrade pip + install the two coordinated packages.
  uv pip install --quiet --upgrade pip
  uv pip install --quiet \
      "autogen-agentchat==${ver}" \
      "autogen-ext[openai]==${ver}"

  deactivate
}

# ── 3. build both environments ──────────────────────────────────────────────
make_env "venv_047" "0.4.7"
make_env "venv_062" "0.6.2"

echo "✅  Environments ready:"
echo "   • ./venv_047  (autogen-agentchat 0.4.7 + autogen-ext[openai] 0.4.7)"
echo "   • ./venv_062  (autogen-agentchat 0.6.2 + autogen-ext[openai] 0.6.2)"
