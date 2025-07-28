# real-estate-price-prediction
real-estate-price-prediction






---

### ✅ **Objective: Scrape all MagicBricks property listings and save**

* **Full HTML page**
* **Embedded JSON data**

---

### 🔁 **Strategy**

MagicBricks uses **infinite scroll**, so we’ll use **Selenium** to:

* Scroll the page repeatedly until no new properties load.
* Extract each property’s container block.

Then for each property:

* **Save full HTML** of the listing.
* **Extract embedded JSON (`<script type="application/ld+json">`)** if available.
* Save JSON separately.

---

### 💡 Suggested Folder Structure

Under `src/scraping/`:

```
src/
 └── scraping/
     ├── scroll_magicbricks.py          ← handles scrolling and listing URL extraction
     ├── save_property_html.py          ← saves raw HTML of each listing
     ├── extract_json_from_html.py      ← parses and saves JSON
     ├── scrape_all_properties.py       ← orchestrator to run all steps
     └── utils/
         ├── file_utils.py              ← write_html(), write_json()
         ├── driver_setup.py            ← Selenium WebDriver setup
```

---

### 📁 Output Storage

```
artifacts/
 ├── raw_html/
 │    ├── property_001.html
 │    ├── ...
 └── json_data/
      ├── property_001.json
      ├── ...
```

---

### ⚙️ Tools & Tech Stack

* **Selenium** (for scroll and dynamic loading)
* **BeautifulSoup** (for HTML parsing)
* **`json` module** (for JSON parsing)
* **Logging** and **Exception Handling** as per your base setup

---

### 🔍 HTML vs JSON — What to Extract?

| Field Type         | Extract From |
| ------------------ | ------------ |
| Title              | HTML         |
| Price              | Both         |
| Location           | JSON         |
| Society            | HTML         |
| Size (sqft)        | HTML         |
| Bedrooms/Bathrooms | HTML         |
| Coordinates        | JSON         |
| Owner/Agent Name   | JSON         |

---
