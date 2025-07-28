from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from src.utils.logger import logger
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_scraper():
    logger.info("Starting MagicBricks scraping...")

    try:
        #url = "https://www.magicbricks.com/ready-to-move-flats-in-hyderabad-pppfs"
        url = "https://www.99acres.com/gated-community-plots-land-in-hyderabad-ffid"

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        sleep(5)

        property_cards = driver.find_elements(By.CLASS_NAME, "mb-srp__card__info")
        logger.info(f"Found {len(property_cards)} properties")

        for card in property_cards[:5]:
            logger.info(f"Property: {card.text.splitlines()[0]}")

        driver.quit()

    except Exception as e:
        logger.exception("Scraping failed")
