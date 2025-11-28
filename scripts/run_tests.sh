#!/bin/bash
# Test runner script for CuratorAI backend

echo "🧪 Running CuratorAI API Tests"
echo "================================"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run pytest with coverage
python -m pytest apps/ \
    --verbose \
    --tb=short \
    --cov=apps \
    --cov-report=html \
    --cov-report=term \
    --cov-report=json \
    -p no:warnings

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report generated in htmlcov/index.html"

