"""
Google Calendar Sync for Beitar Jerusalem Games
Syncs home games at Teddy Stadium to Google Calendar
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']


class CalendarSync:
    """Sync games to Google Calendar"""
    
    def __init__(self, calendar_id: Optional[str] = None, credentials_path: str = 'credentials.json'):
        self.credentials_path = credentials_path
        self.calendar_id = calendar_id or 'primary'
        self.service = self._get_service()
    
    def _get_service(self):
        """Authenticate and return Calendar API service"""
        creds = None
        
        # Load existing token
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # For GitHub Actions, use environment variable
                if os.environ.get('GOOGLE_CREDENTIALS'):
                    creds_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
                    creds = Credentials.from_authorized_user_info(creds_info, SCOPES)
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
            
            # Save token for future runs
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build('calendar', 'v3', credentials=creds)
    
    def create_event(self, game: Dict) -> Dict:
        """Create a calendar event for a game (public calendar only)"""
        if not game.get('datetime'):
            raise ValueError(f"Game has no datetime: {game}")
        
        start_time = game['datetime']
        end_time = start_time + timedelta(hours=2, minutes=30)  # Game ~2.5 hours
        
        event_body = {
            'summary': f'⚽ בית"ר ירושלים vs {game["away"]}',
            'location': 'אצטדיון טדי, ירושלים',
            'description': self._create_description(game),
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Jerusalem',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Jerusalem',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24 * 60},  # 1 day before
                ],
            },
            'colorId': '11',  # Red - important!
            'visibility': 'public',
        }
        
        event = self.service.events().insert(
            calendarId=self.calendar_id,
            body=event_body
        ).execute()
        
        return event
    
    def _create_description(self, game: Dict) -> str:
        """Create event description"""
        return f"""⚠️ אין חניה באזור טדי - הזז את הרכב!"""
    
    def find_existing_event(self, game: Dict) -> Optional[Dict]:
        """Check if event already exists for this game"""
        if not game.get('datetime'):
            return None
        
        # Search for events on the same day with similar title
        start_of_day = game['datetime'].replace(hour=0, minute=0, second=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=start_of_day.isoformat() + 'Z',
            timeMax=end_of_day.isoformat() + 'Z',
            q='בית"ר ירושלים',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Check for matching game
        for event in events:
            if game['away'] in event.get('summary', ''):
                return event
        
        return None
    
    def sync_games(self, games: List[Dict], dry_run: bool = False) -> Dict:
        """Sync games to public calendar, avoiding duplicates"""
        results = {
            'created': [],
            'existing': [],
            'failed': [],
            'dry_run': dry_run
        }
        
        for game in games:
            try:
                # Check if already exists
                existing = self.find_existing_event(game)
                
                if existing:
                    results['existing'].append({
                        'game': game,
                        'event_id': existing['id']
                    })
                    print(f"⏭️  Already exists: {game['home']} vs {game['away']}")
                    continue
                
                if dry_run:
                    print(f"🔍 [DRY RUN] Would create: {game['home']} vs {game['away']}")
                    results['created'].append({'game': game, 'event_id': 'dry-run'})
                else:
                    event = self.create_event(game)
                    results['created'].append({
                        'game': game,
                        'event_id': event['id'],
                        'link': event.get('htmlLink')
                    })
                    print(f"✅ Created: {game['home']} vs {game['away']}")
                    
            except Exception as e:
                results['failed'].append({
                    'game': game,
                    'error': str(e)
                })
                print(f"❌ Failed: {game['home']} vs {game['away']} - {e}")
        
        return results
    
    def delete_all_beitar_events(self, confirm: bool = False) -> int:
        """Delete all Beitar events (for cleanup)"""
        if not confirm:
            print("⚠️  Use confirm=True to actually delete")
            return 0
        
        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            q='בית"ר ירושלים',
            singleEvents=True
        ).execute()
        
        events = events_result.get('items', [])
        deleted = 0
        
        for event in events:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event['id']
            ).execute()
            deleted += 1
            print(f"🗑️  Deleted: {event.get('summary')}")
        
        return deleted


if __name__ == '__main__':
    from scraper import BeitarScraper
    
    print("="*60)
    print("Beitar Jerusalem - Google Calendar Sync")
    print("="*60)
    
    # Fetch games
    scraper = BeitarScraper()
    teddy_games = scraper.get_home_games_at_teddy()
    
    print(f"\nFound {len(teddy_games)} home games at Teddy Stadium")
    
    if not teddy_games:
        print("No games to sync!")
        exit(0)
    
    # Show what will be synced
    print("\nGames to sync:")
    for game in teddy_games:
        print(f"  📅 {game['date_text']}: {game['home']} vs {game['away']}")
    
    # Sync to calendar
    print("\n" + "="*60)
    print("Syncing to Google Calendar...")
    print("="*60)
    
    sync = CalendarSync()
    results = sync.sync_games(teddy_games, dry_run=True)
    
    print(f"\nResults:")
    print(f"  ✅ Created: {len(results['created'])}")
    print(f"  ⏭️  Existing: {len(results['existing'])}")
    print(f"  ❌ Failed: {len(results['failed'])}")
