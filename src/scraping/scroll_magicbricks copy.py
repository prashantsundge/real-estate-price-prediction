
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.utils.logger import logger


def scroll_and_collect_property_cards(base_url:str,scroll_pause=2,max_scrolls=50):
    logger.info("Launching Broswer to scroll MagicBricks...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable_gpu")
    options.add_argument("--no-sandbox")
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(base_url)
    time.sleep() # wait for page to load

    property_cards_set = set()
    last_height = driver.execute_script("return document.body.scrollHeight")


    for scroll_count in range(max_scrolls):
        logger.info(f"Scrolling...{scroll_count+1}/{max_scrolls}")

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(scroll_pause)

        cards = driver.find_elements(By.CLASS_NAME, "mb-srp__card")

       # cards = driver.find_elements(By.CLASS_NAME, "mb-srp__card")
        property_cards_set.update([card.get_attribute("innerHTML") for card in cards])

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logger.info("No more new Content loaded on scroll.")
            break
        last_height = new_height

    logger.info(f"Total unique blocks found : {len(property_cards_set)}")
    driver.quit()

    return list(property_cards_set)



