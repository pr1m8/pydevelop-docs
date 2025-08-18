#!/bin/bash
# Script to serve PyDevelop-Docs documentation in background

# Configuration
DOCS_DIR="/home/will/Projects/haive/backend/haive/tools/pydevelop-docs/docs/build/html"
PORT=8004
LOG_FILE="/tmp/pydevelop_docs_server.log"
PID_FILE="/tmp/pydevelop_docs_server.pid"

# Function to stop existing server
stop_server() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Stopping existing server (PID: $PID)..."
            kill -9 "$PID" 2>/dev/null || true
        fi
        rm -f "$PID_FILE"
    fi
    
    # Also kill any python http.server processes on our port
    lsof -ti:$PORT | xargs -r kill -9 2>/dev/null || true
}

# Function to start server
start_server() {
    echo "Starting PyDevelop-Docs documentation server..."
    
    # Check if docs directory exists
    if [ ! -d "$DOCS_DIR" ]; then
        echo "Error: Documentation directory not found at $DOCS_DIR"
        echo "Please build the documentation first with: poetry run sphinx-build -b html docs/source docs/build"
        exit 1
    fi
    
    # Start server in background
    cd "$DOCS_DIR"
    nohup python -m http.server $PORT > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
    # Save PID
    echo $SERVER_PID > "$PID_FILE"
    
    # Wait a moment and check if server started
    sleep 2
    if ps -p "$SERVER_PID" > /dev/null; then
        echo "✓ Documentation server started successfully!"
        echo "  PID: $SERVER_PID"
        echo "  URL: http://localhost:$PORT"
        echo "  Log: $LOG_FILE"
        echo ""
        echo "To view the documentation, open: http://localhost:$PORT"
        echo "To stop the server, run: $0 stop"
    else
        echo "✗ Failed to start server. Check the log file: $LOG_FILE"
        tail -n 10 "$LOG_FILE"
        exit 1
    fi
}

# Function to check server status
check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Documentation server is running (PID: $PID)"
            echo "URL: http://localhost:$PORT"
        else
            echo "Documentation server is not running (stale PID file)"
            rm -f "$PID_FILE"
        fi
    else
        echo "Documentation server is not running"
    fi
}

# Main script logic
case "${1:-start}" in
    start)
        stop_server
        start_server
        ;;
    stop)
        stop_server
        echo "Documentation server stopped"
        ;;
    restart)
        stop_server
        start_server
        ;;
    status)
        check_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the documentation server (default)"
        echo "  stop    - Stop the documentation server"
        echo "  restart - Restart the documentation server"
        echo "  status  - Check if the server is running"
        exit 1
        ;;
esac