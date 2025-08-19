#!/bin/bash
cd /home/will/Projects/haive/backend/haive
export PATH="/home/will/Projects/haive/backend/haive/tools/pydevelop-docs/.venv/bin:$PATH"
poetry run --directory=/home/will/Projects/haive/backend/haive/tools/pydevelop-docs pydevelop-docs rebuild-haive --debug --save-log