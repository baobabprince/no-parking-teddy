"""
Beitar Jerusalem Games Scraper
Scrapes game schedule from beitarfc.co.il and filters for home games at Teddy Stadium
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import re


class BeitarScraper:
    """Scraper for Beitar Jerusalem game schedule"""
    
    URL = "https://www.beitarfc.co.il/%D7%9E%D7%A9%D7%97%D7%A7%D7%99%D7%9D/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def fetch_games(self) -> List[Dict]:
        """Fetch all games from the website"""
        response = self.session.get(self.URL)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        games = []
        
        for game_div in soup.find_all('div', class_='game_list_item'):
            game = self._parse_game(game_div)
            if game:
                games.append(game)
        
        return games
    
    def _parse_game(self, game_div) -> Optional[Dict]:
        """Parse a single game element"""
        # Team names
        teams_names = game_div.find('div', class_='teams_names')
        if not teams_names:
            return None
        
        home_team = teams_names.find('div', class_='home')
        away_team = teams_names.find('div', class_='away')
        
        home = home_team.get_text(strip=True) if home_team else None
        away = away_team.get_text(strip=True) if away_team else None
        
        if not home or not away:
            return None
        
        # Game info
        game_info = game_div.find('div', class_='game_info')
        
        stadium = None
        date_str = None
        game_round = None
        
        if game_info:
            stadium_el = game_info.find('div', class_='stadium')
            date_el = game_info.find('div', class_='date')
            round_el = game_info.find('div', class_='round')
            
            stadium = stadium_el.get_text(strip=True) if stadium_el else None
            date_str = date_el.get_text(strip=True) if date_el else None
            game_round = round_el.get_text(strip=True) if round_el else None
        
        # Parse date
        game_datetime = self._parse_date(date_str)
        
        return {
            'home': home,
            'away': away,
            'stadium': stadium,
            'date_text': date_str,
            'datetime': game_datetime,
            'round': game_round,
            'is_home_game': 'בית"ר ירושלים' in home
        }
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string like '08/02/26 -> 01:59' to datetime"""
        if not date_str:
            return None
        
        try:
            # Format: "08/02/26 -> 01:59"
            match = re.search(r'(\d{2})/(\d{2})/(\d{2})\s*->\s*(\d{2}):(\d{2})', date_str)
            if match:
                day, month, year_short, hour, minute = match.groups()
                year = int(year_short) + 2000  # 26 -> 2026
                return datetime(year, int(month), int(day), int(hour), int(minute))
        except Exception as e:
            print(f"Error parsing date '{date_str}': {e}")
        
        return None
    
    def get_home_games_at_teddy(self, games: List[Dict] = None) -> List[Dict]:
        """Filter for home games at Teddy Stadium"""
        if games is None:
            games = self.fetch_games()
        
        teddy_games = []
        for game in games:
            if (game['is_home_game'] and 
                game['stadium'] and 
                'טדי' in game['stadium']):
                teddy_games.append(game)
        
        return teddy_games


if __name__ == '__main__':
    scraper = BeitarScraper()
    
    print("Fetching all games...")
    all_games = scraper.fetch_games()
    
    print(f"\nFound {len(all_games)} total games:")
    for game in all_games:
        home_away = "🏠 HOME" if game['is_home_game'] else "✈️ AWAY"
        print(f"  {game['home']} vs {game['away']} - {game['stadium']} ({home_away})")
    
    print("\n" + "="*50)
    print("Home games at Teddy Stadium (NO PARKING!):")
    print("="*50)
    
    teddy_games = scraper.get_home_games_at_teddy(all_games)
    for game in teddy_games:
        print(f"\n⚽ {game['home']} vs {game['away']}")
        print(f"   📅 {game['date_text']}")
        print(f"   🏟️  {game['stadium']}")
        print(f"   🅿️  NO PARKING - Move your car!")
