#!/usr/bin/env bash
set -e
root=$(cd $(dirname $(readlink $0 || echo $0))/..;/bin/pwd)

echo "root path: ${root}"

if [[ ! -d "${root}/venv" ]]; then
  echo "install virtual env"
  python3 -m venv "${root}/.venv"
fi

source  ${root}/.venv/bin/activate

uv sync

export PYTHONPATH=${PYTHONPATH}:${root}:${root}/ai_model:${root}/projects:${root}/simple_agent

if [[ ! -f "${root}/.git/hooks/pre-commit" ]]; then
  pre-commit install
fi
