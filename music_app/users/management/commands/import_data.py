import os
import subprocess
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Import data from SQL file if not already imported'

    def handle(self, *args, **options):
        # Sprawdź czy dane już są
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users_user")
            user_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM music_track")
            track_count = cursor.fetchone()[0]
        
        if user_count > 1:  
            self.stdout.write(self.style.WARNING('Data already imported, skipping...'))
            self.stdout.write(f'   Users: {user_count}')
            self.stdout.write(f'   Tracks: {track_count}')
            return
        
        sql_file = '/app/database_data_only.sql'
        
        if not os.path.exists(sql_file):
            self.stdout.write(self.style.WARNING('No data file found, starting with empty database'))
            return
        
        self.stdout.write('🔄 Importing database data...')
        
        try:
            # Import SQL
            result = subprocess.run(
                ['psql', '-U', 'musicuser', '-d', 'musicdb', '-f', sql_file],
                env={
                    'PGPASSWORD': 'strongpassword',
                    'PGHOST': 'db',
                },
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
                
                # Pokaż statystyki
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM users_user")
                    users = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM music_track")
                    tracks = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM groups_group")
                    groups = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM events_event")
                    events = cursor.fetchone()[0]
                
                self.stdout.write(self.style.SUCCESS('Imported data:'))
                self.stdout.write(f'   - Users: {users}')
                self.stdout.write(f'   - Tracks: {tracks}')
                self.stdout.write(f'   - Groups: {groups}')
                self.stdout.write(f'   - Events: {events}')
            else:
                self.stdout.write(self.style.ERROR(f'Import failed: {result.stderr}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))