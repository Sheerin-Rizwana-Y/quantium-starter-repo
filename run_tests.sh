#!/usr/bin/env bash

echo "Activating virtual environment..."

# Activate virtual environment (Windows Git Bash)
source venv/Scripts/activate

if [ $? -ne 0 ]; then
  echo "Failed to activate virtual environment"
  exit 1
fi

echo "Running test suite..."

pytest

TEST_STATUS=$?

if [ $TEST_STATUS -eq 0 ]; then
  echo "All tests passed!"
  exit 0
else
  echo "Tests failed!"
  exit 1
fi
