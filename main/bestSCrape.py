import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
from datetime import datetime
import pandas as pd
from pymongo import MongoClient

class BetikaScraper:
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    DB_NAME = 'clash'
    COLLECTION_NAME = 'games'
    #myclient=MongoClient(MONGODB_HOST,MONGODB_PORT)
   # mongodb+srv://EngCapiyo:Capiyo%401010@cluster1.kbtey0y.mongodb.net/Solvus?retryWrites=true&w=majority&appName=Cluster1
    myclient = MongoClient("mongodb+srv://EngCapiyo:Capiyo%401010@cluster1.kbtey0y.mongodb.net/Solvus?retryWrites=true&w=majority&appName=Cluster1", tls=True, tlsAllowInvalidCertificates=True)
  # mongodb+srv://apiyoosca_db_user:<db_password>@cluster1.llv3sbb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1
   
    mydb = myclient["clash"]
    mycol = mydb["fixtures"]
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        
        # Basic options to avoid detection
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Headless mode (comment out for debugging)
        chrome_options.add_argument("--headless")
        
        # User agent to mimic real browser
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Additional anti-detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def scrape_today_fixtures(self):
        """Scrape today's football fixtures from Betika"""
        try:
            # Navigate to Betika football page
            url = "https://www.betika.com/en-ke/s/soccer"
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "prebet-match"))
            )
            
            # Give some time for dynamic content to load
            time.sleep(5)
            
            fixtures = []
            
            # Find all match containers
            match_containers = self.driver.find_elements(By.CLASS_NAME, "prebet-match")
            
            for match in match_containers:
                try:
                    fixture_data = self.extract_match_data(match)
                    if fixture_data:
                        fixtures.append(fixture_data)
                        self.mycol.insert_one(fixture_data)
                        
               
                    
                        
                        #print(fixtures)
            
                except Exception as e:
                    print(f"Error extracting match data: {e}")
                    continue
           # print(fixtures)        
            return fixtures
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            return []
    
    def extract_match_data(self, match_element):
        """Extract data from a single match element"""
        try:
            # Extract teams
            teams_element = match_element.find_element(By.CLASS_NAME, "prebet-match__teams")
            #my_league =match_element.find_element(By.CLASS_NAME, "pull-left")
            
            #home_team = teams_element.find_element(By.CLASS_NAME, "prebet-match__teams__home").text
            #away_team = teams_element.find_element(By.CSS_SELECTOR, "span[prebet-match__teams]").text
            
            team_spans = teams_element.find_elements(By.TAG_NAME, "span")
    
    # Assuming home team is first span, away team is second span
            if len(team_spans) >= 2:
              home_team = team_spans[0].text
              away_team = team_spans[1].text
              
              games={
                "homeTeam":home_team,"awayTeam":away_team,
                
                }
              
             
              
              
            else:
             pass
            
            # Extract time
            team_spans = teams_element.find_elements(By.TAG_NAME, "span")
            time_element = match_element.find_element(By.CLASS_NAME, "time")
            match_time = time_element.text
            
            parts = match_time.splitlines()
            league = parts[0]  # 'International Clubs • CAF Cham...'
            date_time = parts[1]
            
            
            
            
            # Extract odds (if available)
            odds = {}
            try:
                odds_elements = match_element.find_elements(By.CLASS_NAME, "prebet-match__odd")
                if len(odds_elements) >= 3:
                    odds = {
                        'home_win': odds_elements[0].text,
                        'draw': odds_elements[1].text,
                        'away_win': odds_elements[2].text
                    }
            except:
                odds = {'home_win': 'N/A', 'draw': 'N/A', 'away_win': 'N/A'}
            
            # Extract league information
           # league = "Unknown"
            try:
                league_element = match_element.find_element(By.CLASS_NAME, "prebet-match__competition")
                league = league_element.text
               
            except:
                pass
            
            fixture = {
            
                'home_team': home_team.strip(),
                'away_team': away_team.strip(),                              
                'league':league,
                "home_win":odds["home_win"],
                "away_win":odds['away_win'],
                "draw":odds["draw"],
                'date': date_time
            }
            
              
            
            
            
            
            
            
            
            
            return fixture
           
        except Exception as e:
            print(f"Error in extract_match_data: {e}")
            return None
    
    def save_to_json(self, fixtures, filename=None):
        """Save fixtures to JSON file"""
        if filename is None:
            filename = f"betika_fixtures_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
        print(f"Fixtures saved to {filename}")
    
    def save_to_csv(self, fixtures, filename=None):
        """Save fixtures to CSV file"""
        if filename is None:
            filename = f"betika_fixtures_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Flatten the odds data for CSV
        flattened_data = []
        for fixture in fixtures:
            flat_fixture = {
                'home_team': fixture['home_team'],
                'away_team': fixture['away_team'],
                'match_time': fixture['match_time'],
                'league': fixture['league'],
                'home_win_odds': fixture['odds']['home_win'],
                'draw_odds': fixture['odds']['draw'],
                'away_win_odds': fixture['odds']['away_win'],
                'scraped_at': fixture['scraped_at']
            }
            flattened_data.append(flat_fixture)
        
        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Fixtures saved to {filename}")
    
    def display_fixtures(self, fixtures):
        """Display fixtures in a readable format"""
        print(f"\n{'='*80}")
        print(f"BETIKA TODAY'S FIXTURES - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*80}")
        
        for i, fixture in enumerate(fixtures, 1):
            print(f"\n{i}. {fixture['home_team']} vs {fixture['away_team']}")
            print(f"   Time: {fixture['match_time']}")
            print(f"   League: {fixture['league']}")
            print(f"   Odds: Home {fixture['odds']['home_win']} | Draw {fixture['odds']['draw']} | Away {fixture['odds']['away_win']}")
            print(f"   {'-'*50}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

# Alternative approach using API (if available)
def try_api_approach():
    """Try to get data through API calls if available"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.betika.com/',
    }
    
    # Betika might have internal API endpoints
    api_urls = [
        "https://api.betika.com/v1/matches",
        "https://www.betika.com/api/v1/matches",
        "https://betika.com/api/v1/fixtures"
    ]
    
    for url in api_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("API data found!")
                print(data)
                return data
        except:
            continue
    
    return None

def main():
    """Main function to run the scraper"""
    scraper = None
    try:
        print("Starting Betika scraper...")
        
        # First try API approach (less intrusive)
        print("Trying API approach...")
        api_data = try_api_approach()
        
        if api_data:
            print("Successfully retrieved data via API")
            # Process API data here
            return
        
        # If API fails, use Selenium
        print("API approach failed, using Selenium...")
        scraper = BetikaScraper()
        
        print("Scraping today's fixtures...")
        fixtures = scraper.scrape_today_fixtures()
        
        if fixtures:
            print(f"Successfully scraped {len(fixtures)} fixtures!")
            
            # Display fixtures
            scraper.display_fixtures(fixtures)
            
            # Save to files
            scraper.save_to_json(fixtures)
            scraper.save_to_csv(fixtures)
            
        else:
            print("No fixtures found or scraping failed.")
            
    except Exception as e:
        print(f"Error in main: {e}")
        
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
  games=BetikaScraper()
  games.scrape_today_fixtures()