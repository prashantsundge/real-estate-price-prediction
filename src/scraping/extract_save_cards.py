
import os 
import json
from bs4 import BeautifulSoup
from src.utils.logger import logger


#directories to save raw data

html_dir = "data/raw/extracted_html"
json_dir = "data/raw/extracted_json"

os.makedirs(html_dir, exist_ok=True)
os.makedirs(json_dir, exist_ok=True)

def extract_json_from_html(html_content):
    """
    Extract JSON-LD data from HTML content.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    json_ld_tag = soup.find("script", {"type":"application/ld+json"})
    if json_ld_tag:
        try:
            return json.loads(json_ld_tag.string)
        except Exception as e:
            logger.warning(f"Error Parsing JSON_LD: {e}")

    return None
def save_card_data(card_element, index):
    """
    Save HTML and extracted JSON of a property card.
    """

    html_content = str(card_element)

    html_path = os.path.join(html_dir, f"card_{index}.html")
    with open(html_path, "w" , encoding="utf-8") as f:
        f.write(html_content)

    json_data = extract_json_from_html(html_content)
    if json_data:
        json_path = os.path.join(json_dir, f"card_{index}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)


    logger.info(f"Saved card {index} : HTML and JSON")

def extract_and_save_cards(card_elements):
    """
    Iterate over all cards and save thier data.

    """
    logger.info(f"Extracting and saving {len(card_elements)} cards...")
    for idx, card in enumerate(card_elements):
        save_card_data(card, idx)
    logger.info("ALL cards Saved Successfully .")
    