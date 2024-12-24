#!/bin/sh

set -e

export PYTHONPATH=/app:$PYTHONPATH

# Function to check if migrations directory exists
check_migrations() {
    if [ ! -d "/app/migrations" ]; then
        echo "Initializing migrations directory..."
        FLASK_APP="app:create_app()" flask db init
    else
        echo "Migrations directory already exists"
    fi
}

# Function to check if database is ready


# Initialize migrations if needed
check_migrations

# Wait for database

echo "Running database migrations..."
# Create a new migration if there are changes
if FLASK_APP="app:create_app()" flask db migrate -m "Auto migration" 2>&1 | grep -q "No changes detected"; then
    echo "No schema changes detected"
else
    echo "New migration created"
fi

# Try to upgrade
if FLASK_APP="app:create_app()" flask db upgrade; then
    echo "Database upgrade successful"
else
    echo "Database upgrade failed"
    exit 1
fi

# Start the Flask application
echo "Starting Flask application..."
FLASK_APP="app:create_app()" exec flask run --host=0.0.0.0 --port=5000