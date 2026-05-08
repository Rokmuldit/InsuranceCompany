#!/bin/sh

# Stop execution if any command fails
set -e

echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
