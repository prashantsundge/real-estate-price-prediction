import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# Logger Setup
from src.utils.logger import logger


# Function to scrape listings from MagicBricks or 99acres
def scrape_listings(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Failed to fetch data from {url} with status code {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        listings = []

        # Scrape properties (adjust based on the site's HTML structure)
        for property in soup.find_all('div', class_="property-card"):
            title = property.find('h2', class_="title").text.strip() if property.find('h2', class_="title") else None
            price = property.find('div', class_="price").text.strip() if property.find('div', class_="price") else None
            location = property.find('span', class_="location").text.strip() if property.find('span', class_="location") else None
            area = property.find('span', class_="area").text.strip() if property.find('span', class_="area") else None
            property_type = property.find('span', class_="type").text.strip() if property.find('span', class_="type") else None
            amenities = property.find('div', class_="amenities").text.strip() if property.find('div', class_="amenities") else None
            agent = property.find('div', class_="agent-name").text.strip() if property.find('div', class_="agent-name") else None

            listings.append({
                'title': title,
                'price': price,
                'location': location,
                'area': area,
                'property_type': property_type,
                'amenities': amenities,
                'agent': agent
            })
        
        logger.info(f"Successfully scraped {len(listings)} properties")
        return listings

    except Exception as e:
        logger.error(f"Error occurred while scraping: {str(e)}")
        return []

# Example usage
if __name__ == "__main__":
    url = "https://www.magicbricks.com/property-for-sale/residential-commercial-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/Godown,Industrial-Building,Industrial-Shed&BudgetMin=1-Crores&BudgetMax=1.5-Crores&cityName=Hyderabad"  # Change to target page
    listings = scrape_listings(url)

    # Save the data to CSV or directly push to SQL later
    if listings:
        import pandas as pd
        df = pd.DataFrame(listings)
        df.to_csv(f"data/raw/scraped_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)
        logger.info("Data saved to CSV.")
