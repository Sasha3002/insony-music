#!/bin/bash
# init_db.sh - Automatic database import on first run

echo "Checking for database backup..."

if [ -f /docker-entrypoint-initdb.d/database_data_only.sql ]; then
    echo "Waiting for Django migrations to complete..."
    
    for i in {1..60}; do
        if psql -U musicuser -d musicdb -c "SELECT 1 FROM users_user LIMIT 1;" > /dev/null 2>&1; then
            echo "Django tables detected!"
            break
        fi
        sleep 1
    done
    
    echo "Importing database data..."
    psql -U musicuser -d musicdb -f /docker-entrypoint-initdb.d/database_data_only.sql > /var/log/import.log 2>&1
    
    if [ $? -eq 0 ]; then
        echo "Database data imported successfully!"
        echo "Available data:"
        echo "   - Users: $(psql -U musicuser -d musicdb -t -c 'SELECT COUNT(*) FROM users_user;' | xargs)"
        echo "   - Tracks: $(psql -U musicuser -d musicdb -t -c 'SELECT COUNT(*) FROM music_track;' | xargs)"
        echo "   - Groups: $(psql -U musicuser -d musicdb -t -c 'SELECT COUNT(*) FROM groups_group;' | xargs)"
        echo "   - Events: $(psql -U musicuser -d musicdb -t -c 'SELECT COUNT(*) FROM events_event;' | xargs)"
    else
        echo "Import failed! Check /var/log/import.log"
    fi
else
    echo "No data backup found - starting with empty database"
fi