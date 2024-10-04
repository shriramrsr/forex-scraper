# scraper/scraper.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models import insert_forex_rate
from apscheduler.schedulers.background import BackgroundScheduler
from config import CURRENCY_PAIRS

def scrape_forex_rates():
    try:
        url = "https://www.x-rates.com/table/?from=USD&amount=1"
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the response was unsuccessful
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='tablesorter ratesTable')
        if table is None:
            raise ValueError("Could not find the rates table on the page.")

        rates = {}
        rows = table.find_all('tr')[1:]  # Skip header row

        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 3:
                currency = cols[0].text.strip()
                rate = float(cols[1].text.strip())
                rates[currency] = rate
            else:
                print(f"Skipping invalid row: {row}")
    except Exception as e:
        print(f"Error parsing HTML or extracting forex rates: {e}")
        return

    date = datetime.now().date()

    try:
        print(rates)
        for country in rates.keys():
            insert_forex_rate(date, "USA", country, float(rates[country]))
        # for base, quote in CURRENCY_PAIRS:
        #     if base == 'USD':
        #         rate = rates.get(quote)
        #     elif quote == 'USD':
        #         rate = 1 / rates.get(base)
        #     else:
        #         rate = rates.get(quote) / rates.get(base)
            
        #     if rate:
        #         insert_forex_rate(date, base, quote, rate)
        #     else:
        #         print(f"No rate found for {base}/{quote} on {date}")
    except Exception as e:
        print(f"Error calculating or inserting forex rates: {e}")

# scraper/scheduler.py

# from scraper.scraper import scrape_forex_rates

def start_scheduler():
    # try:
    #     scrape_forex_rates()
    #     print("Scraped successfully")
    # except Exception as e:
    #     print(f"Scraping Failed: {e}")

    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_forex_rates, 'cron', hour=6)
    scheduler.start()