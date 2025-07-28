from bs4 import BeautifulSoup


#load Saved HTML 

with open("magicbricks_page.html" , "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

#try to locate property cards 

property_cards = soup.find_all("div" , class_="mb-srp__card")

print(f"Total Properties found : {len(property_cards)}")

if property_cards:
    first = property_cards[0]

    title = first.find("h2")
    title=title.text.strip() if title else "N/A"

    price = first.find("div", class_="mb-srp__card__price--amount")
    price = price.text.strip() if price else "N/A"

    # Try different classes for location
    location = first.find("div", class_="mb-srp__card__address") or \
            first.find("div", class_="mb-srp__card__location") or \
            first.find("div", class_="mb-srp__card--desc__loc")

    location = location.text.strip() if location else "N/A"



    print("\n--- Sample Listing ---")
    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Location: {location}")
    
    print(first.prettify())
else:
    print("⚠️ No property cards found. Check the HTML or website structure.")