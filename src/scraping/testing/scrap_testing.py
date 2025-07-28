from  selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

#setup chrome options
options = Options()
options.add_argument("__headless")
options.add_argument("__no-sandbox")
options.add_argument("__disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


#url = "https://www.magicbricks.com/property-for-sale/residential-commercial-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/Godown,Industrial-Building,Industrial-Shed&BudgetMin=1-Crores&BudgetMax=1.5-Crores&cityName=Hyderabad"

url = "https://www.magicbricks.com/flats-in-hyderabad-for-sale-pppfs"

#url = "https://www.99acres.com/gated-community-plots-land-in-hyderabad-ffid"

driver.get(url)
time.sleep(5)
with open("magicbricks_page.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
print("Page HTML saved to magicbricks.html")