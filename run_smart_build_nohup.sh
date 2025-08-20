#!/bin/bash
# Run smart documentation build with nohup for long-running process

echo "🚀 Starting Smart Documentation Build with nohup"
echo "📁 Output will be in: smart_docs_build/"
echo "📋 Logs will be in: smart_build.log"
echo ""

# Create output directory
mkdir -p smart_docs_build

# Run with nohup
nohup python run_smart_build.py > smart_build.log 2>&1 &

# Get the PID
PID=$!
echo "🏃 Build started with PID: $PID"
echo ""
echo "Monitor progress with:"
echo "  tail -f smart_build.log"
echo "  tail -f smart_docs_build/*/build_progress.log"
echo ""
echo "Check build status:"
echo "  cat smart_docs_build/build_results.json | jq '.summary'"
echo ""
echo "Kill if needed:"
echo "  kill $PID"