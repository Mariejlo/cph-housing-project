# Web scraping script for housing data

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL and headers
BASE_URL = "https://www.boligsiden.dk/salg/resultat"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
}

# Define the parameters for scraping
PARAMS = {
    "postnummer": ["2650", "2500"],  # Hvidovre and Valby postal codes
    "antalVaerelserMin": "3",
    "antalVaerelserMax": "3",
    "type": "ejerlejlighed",  # Owner-occupied apartments
    "side": 1  # Start with the first page
}

# Function to extract listings from a page
def extract_listings(soup):
    listings = []
    property_cards = soup.find_all("div", class_="search-result-item")  # Adjust the class if needed
    for card in property_cards:
        try:
            price = card.find("div", class_="list-item-price").text.strip()
            address = card.find("div", class_="list-item-address").text.strip()
            size = card.find("div", class_="list-item-area").text.strip()
            rooms = card.find("div", class_="list-item-rooms").text.strip()
            listings.append({
                "Price": price,
                "Address": address,
                "Size": size,
                "Rooms": rooms
            })
        except AttributeError:
            continue
    return listings

# Main scraping logic
def scrape_housing_data():
    all_listings = []
    for page in range(1, 6):  # Adjust the range to scrape more pages
        print(f"Scraping page {page}...")
        PARAMS["side"] = page
        response = requests.get(BASE_URL, headers=HEADERS, params=PARAMS)
        soup = BeautifulSoup(response.text, "html.parser")
        listings = extract_listings(soup)
        all_listings.extend(listings)
        time.sleep(2)  # Avoid overloading the server
    return pd.DataFrame(all_listings)

# Save data to CSV
if __name__ == "__main__":
    data = scrape_housing_data()
    data.to_csv("data/housing_data.csv", index=False)
    print("Data saved to data/housing_data.csv!")
    