#!/bin/bash
cd /home/will/Projects/haive/backend/haive
export PATH="/home/will/Projects/haive/backend/haive/tools/pydevelop-docs/.venv/bin:$PATH"
export PYTHONPATH="/home/will/Projects/haive/backend/haive/tools/pydevelop-docs/src:$PYTHONPATH"
poetry run --directory=/home/will/Projects/haive/backend/haive/tools/pydevelop-docs pydevelop-docs build-all --clean --ignore-warnings