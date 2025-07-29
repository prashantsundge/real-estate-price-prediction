import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from src.utils.logger import logger


def scroll_and_collect_property_cards(url, scroll_limit=50, scroll_pause=2):
    logger.info("Launching Broswer to scroll MagicBricks...")

    # chrome_options = Options()
    # #chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    options = Options()
    options.add_argument("--headless=new")  # Enable headless mode (remove this line to disable)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")  # Optional but recommended for full rendering
    options.add_argument("--disable-dev-shm-usage")  # Avoid /dev/shm size issues in containers
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/114.0.5735.199 Safari/537.36")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    cards = driver.find_elements(By.CLASS_NAME, "mb-srp__card")
    print(f"CARDS IMMEDIATELY AFTER LOAD: {len(cards)}")


    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls_done = 0
    logger.info(f"Scrolled to height: {driver.execute_script('return document.body.scrollHeight')}")


    while scrolls_done < scroll_limit:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        logger.info(f"Scrolled to height: {driver.execute_script('return document.body.scrollHeight')}")
        with open("debug_full_page.html", "w", encoding="utf-8") as f:
             f.write(driver.page_source)



        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logger.info("No more new Content loaded on scroll.")
            break
        last_height = new_height
        scrolls_done += 1
        logger.info(f"Scrolling...{scrolls_done}/{scroll_limit}")
        logger.info(f"Scrolled to height: {driver.execute_script('return document.body.scrollHeight')}")


    soup = BeautifulSoup(driver.page_source, "html.parser")
    cards = soup.find_all("div", class_="mb-srp__card")

    logger.info(f"Total unique blocks found : {len(cards)}")

    html_dir = "data/raw/html"
    json_dir = "data/raw/json"
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    for idx, card in enumerate(cards):
        # Save full HTML
        with open(os.path.join(html_dir, f"card_{idx+1}.html"), "w", encoding="utf-8") as f:
            f.write(str(card))

        # Save embedded JSON if found
        script_tag = card.find("script", type="application/ld+json")
        if script_tag:
            with open(os.path.join(json_dir, f"card_{idx+1}.json"), "w", encoding="utf-8") as f:
                f.write(script_tag.string.strip())

    driver.quit()
    return cards
