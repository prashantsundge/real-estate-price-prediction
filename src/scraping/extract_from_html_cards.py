import os
import pandas as pd
from bs4 import BeautifulSoup
from src.utils.logger import logger

from src.database.connection import engine


def extract_features_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    try:
        title = soup.find("h2", class_="mb-srp__card--title")
        title = title.text.strip() if title else None

        price = soup.find("div", class_="mb-srp__card__price--amount")
        price = price.text.strip().replace("\u20b9", "").replace(",", "") if price else None

        description_tag = soup.find("div", class_="mb-srp__card--desc--text")
        description = description_tag.p.text.strip() if description_tag and description_tag.p else None

        summary = soup.find("div", class_="mb-srp__card__summary__list")
        summary_items = summary.find_all("div", class_="mb-srp__card__summary__list--item") if summary else []

        summary_dict = {}
        for item in summary_items:
            label = item.find("div", class_="mb-srp__card__summary--label")
            value = item.find("div", class_="mb-srp__card__summary--value")
            if label and value:
                summary_dict[label.text.strip()] = value.text.strip()

        super_area = summary_dict.get("Super Area")

        possession = None
        if "Under Construction" in html_content:
            possession_tag = soup.find("div", string=lambda text: text and "Poss." in text)
            possession = possession_tag.text.strip() if possession_tag else None

        parking = summary_dict.get("Car Parking")

        price_per_sqft_tag = soup.find("div", class_="mb-srp__card__price--size")
        price_per_sqft = price_per_sqft_tag.text.strip().replace("₹", "").replace(",", "") if price_per_sqft_tag else None

        society_tag = soup.find("a", class_="mb-srp__card__society--name")
        society = society_tag.text.strip() if society_tag else None

        return {
            "Title": title,
            "Price (INR)": price,
            "Description": description,
            "Carpet Area": summary_dict.get("Carpet Area"),
            "Super Area": super_area,
            "Transaction": summary_dict.get("Transaction"),
            "Furnishing": summary_dict.get("Furnishing"),
            "Bathroom": summary_dict.get("Bathroom"),
            "Possession": possession,
            "Car Parking": parking,
            "Price per Sqft": price_per_sqft,
            "Society": society
        }

    except Exception as e:
        logger.warning(f"Failed to parse HTML block: {e}")
        return {}

def parse_all_html_cards(input_dir="data/raw/extracted_html", output_csv="data/processed/html_data.csv"):
    all_data = []

    logger.info(f"Parsing HTML cards from {input_dir}")
    for filename in os.listdir(input_dir):
        if filename.endswith(".html"):
            path = os.path.join(input_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
                features = extract_features_from_html(html)
                if features:
                    all_data.append(features)

    df = pd.DataFrame(all_data)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    logger.info(f"Saved parsed HTML data to: {output_csv}")
    print(df.head())

def save_to_mysql(df, table_name="properties"):
    df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
    print(f"SQL DATA INSERTED SUCEESSFULLY ")
    logger.info(f"SQL data inserted")
