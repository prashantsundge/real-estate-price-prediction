
import os 
import json
import pandas as pd
from src.utils.logger import logger

#path to raw json files
RAW_JSON_DIR = "data/raw/extracted_json"

#cleaned Data path for cleaned CSV 

CLEANED_DATA_PATH = "data\processed\cleaned_property_data.csv"
os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)


def load_all_json_files(directory):
    """
    Load all JSON files from a directory into list of dictss

    """
    json_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            try: 
                with open(os.path.join(directory, filename), "r", encoding="utf-8")as f:
                    data = json.load(f)
                    json_data.append(data)
            except Exception as e:
                logger.warning(f"Error reading {filename}: {e}")
    logger.info(f"Loaded {len(json_data)} JSON files from {directory}")
    return json_data

def parse_property_data(json_records):
    """
    Extract Important records from json records
    """
    cleaned_data=[]
    for entry in json_records:
        try:
            property_data ={

                "title" : entry.get("name"),
                "description": entry.get("description"),
                "address": entry.get("address" , {}).get("streetAddress"),
                "locality": entry.get("address" , {}).get("addressLocality"),
                "region": entry.get("address", {}).get("addressRegion"),
                "latitude": entry.get("geo", {}).get("latitude"),
                "longitude": entry.get("geo", {}).get("longitude"),
                "price": entry.get("offers", {}).get("price"),
                "currency": entry.get("offers", {}).get("priceCurrency"),
                "propertyType": entry.get("@type"),
                "postedBy": entry.get("seller", {}).get("@type"),
                "sellerName": entry.get("seller", {}).get("name"),
                "url": entry.get("url")
                
            }
            cleaned_data.append(property_data)
        except Exception as e:
            logger.warning(f"FAILED to PARSE ENTRY : {e}")
    return pd.DataFrame(cleaned_data)

def save_cleaned_data(df):
    """
    Save the cleaned dataframe to csv file
    """
    df.to_csv(CLEANED_DATA_PATH, index=False)
    logger.info(f"Saved Cleaned Data to {CLEANED_DATA_PATH} with {len(df)} records")

