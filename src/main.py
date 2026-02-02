"""
Main entry point for Beitar Calendar Sync
Run this to sync games to Google Calendar
"""

import os
import sys
import json
from scraper import BeitarScraper
from calendar_sync import CalendarSync


def main():
    """Main function"""
    print("="*70)
    print("🏟️  Beitar Jerusalem - Teddy Stadium Parking Alert")
    print("="*70)
    print()
    
    # Check for dry run mode
    dry_run = os.environ.get('DRY_RUN', 'false').lower() == 'true'
    if dry_run:
        print("🔍 DRY RUN MODE - No actual changes will be made")
        print()
    
    # Step 1: Scrape games
    print("📡 Fetching games from beitarfc.co.il...")
    scraper = BeitarScraper()
    
    try:
        all_games = scraper.fetch_games()
        print(f"✅ Found {len(all_games)} total games")
    except Exception as e:
        print(f"❌ Failed to fetch games: {e}")
        sys.exit(1)
    
    # Step 2: Filter for home games at Teddy
    teddy_games = scraper.get_home_games_at_teddy(all_games)
    print(f"🏠 Found {len(teddy_games)} home games at Teddy Stadium")
    print()
    
    if not teddy_games:
        print("ℹ️  No home games at Teddy to sync")
        print("   (This might be during off-season or all games are away)")
        return
    
    # Display games
    print("="*70)
    print("📋 Games to sync (NO PARKING days):")
    print("="*70)
    for i, game in enumerate(teddy_games, 1):
        print(f"\n{i}. ⚽ {game['home']} vs {game['away']}")
        print(f"   📅 {game['date_text']}")
        print(f"   🏟️  {game['stadium']}")
        print(f"   🅿️  REMINDER: Move your car!")
    
    print()
    
    # Step 3: Sync to Google Calendar
    print("="*70)
    print("📅 Syncing to public calendar...")
    print("="*70)
    
    try:
        sync = CalendarSync()
        results = sync.sync_games(teddy_games, dry_run=dry_run)
        
        # Print results
        print()
        print("="*70)
        print("📊 Sync Results:")
        print("="*70)
        print(f"  ✅ Created: {len(results['created'])}")
        print(f"  ⏭️  Already existed: {len(results['existing'])}")
        print(f"  ❌ Failed: {len(results['failed'])}")
        
        if results['created'] and not dry_run:
            print()
            print("🔗 New events:")
            for item in results['created']:
                if item.get('link'):
                    print(f"   - {item['link']}")
        
        # Exit with error if any failed
        if results['failed']:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Calendar sync failed: {e}")
        sys.exit(1)
    
    print()
    print("="*70)
    print("✅ Done! Your calendar is now synced.")
    print("="*70)


if __name__ == '__main__':
    main()
