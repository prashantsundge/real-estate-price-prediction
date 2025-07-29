import sys
import os 
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.scraping.scroll_magicbricks import scroll_and_collect_property_cards
from src.scraping.extract_save_cards import extract_and_save_cards
from src.scraping.parse_clean_cards import load_all_json_files,parse_property_data,save_cleaned_data
from src.scraping.extract_from_html_cards import parse_all_html_cards
from src.scraping.extract_from_html_cards import save_to_mysql
from src.database.data_loader import load_data_from_mysql
from src.utils.logger import logger
from src.models.train_model import train_model

from fastapi import FastAPI
from src.models.schemas import PropertyFeatures
from src.models.predict_model import predict_price

app = FastAPI(title="Real Estate Price Predictor")


def main():
    try:
        logger.info(">>> 🚀 Starting MagicBricks scraping pipeline <<<")
        
        

    #     url = "https://www.magicbricks.com/property-for-sale/residential-commercial-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/Godown,Industrial-Building,Industrial-Shed&BudgetMin=1-Crores&BudgetMax=1.5-Crores&cityName=Hyderabad"

    #    #path to raw json files
    #     RAW_JSON_DIR = "data/raw/extracted_json"

    #     cleand_df = pd.read_csv(r"data/processed/html_data.csv")

    #    #step 1 Scroll and extract raw HTML cards
    #     card_elements = scroll_and_collect_property_cards(url)
    #     print(f"Fetched {len(card_elements)} cards")
    #     logger.info(f"✅ Total property cards collected: {len(card_elements)}")
    #     #step 2 Save individual HTML adn JSON for each card
    #     extract_and_save_cards(card_elements)
    #     logger.info(f"Property Cards Saved to Disk (HTML & JSON)")
    #     #step3 Starting Property JSON cleaning process
    #     logger.info("*** Starting property JSON cleaning process *** ")
    #     raw_json = load_all_json_files(RAW_JSON_DIR)
    #     df = parse_property_data(raw_json)
    #     logger.info(f"Parsed DataFrame Shape :{df.shape}")
    #     save_cleaned_data(df)
    #     logger.info("*** JSON Cleaning and Normalization complete ***")
    #     #step 4 
    #     logger.info(">>> STARTING HTML CARD EXTRACTION <<<")
    #     parse_all_html_cards()
    #     logger.info(">>> HTML CARD EXTRACTION COMPLETED <<<")  
    #     #step 5 
        # logger.info(">>> DATA INSERTION STARTED IN SQL <<<") 
        # save_to_mysql(cleand_df)
        # logger.info(">>> DATA INSERTION COMPLETED IN SQL <<<") 

        # logger.info(">>> DATA LOADING FROM SQL TABLE TO DATAFRAME <<<") 
        # load_df = load_data_from_mysql("properties")
        # logger.info(">>> DATA LOADING FROM SQL TABLE TO DATAFRAME COMPLETED <<<") 
        # print(load_df.info())
        # logger.info("MODEL TRAINING STARTED...")
        # train_model()
        # logger.info("MODEL TRAINING COMPLETED...")
        
      
                
        logger.info("PIPELINE COMPLETED SUCCESSFULLY !.")
    except Exception as e:
        logger.exception("Pipeline failed due to an error. ")

     


if __name__ =="__main__":
    main()
