#!/bin/bash
set -e

echo "Starting FamilyMan UI services..."

# Start the FastAPI agent in the background
echo "Starting FastAPI agent on port ${PYTHON_PORT:-8001}..."
cd /app/agent
python main.py &
AGENT_PID=$!

# Wait for agent to be ready
echo "Waiting for agent to be ready..."
timeout 60 sh -c 'until nc -z localhost 8001; do sleep 1; done' || {
    echo "ERROR: Agent failed to start within 60 seconds"
    kill $AGENT_PID 2>/dev/null || true
    exit 1
}
echo "Agent is ready!"

# Start Next.js in the foreground
echo "Starting Next.js UI on port ${PORT:-3000}..."
cd /app
exec node_modules/.bin/next start -p ${PORT:-3000}
